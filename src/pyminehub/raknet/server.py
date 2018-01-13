import asyncio
from logging import getLogger

from pyminehub.config import ConfigKey, get_value
from pyminehub.network.address import Address, get_unspecified_address, to_packet_format
from pyminehub.network.codec import CompositeCodecContext
from pyminehub.raknet.codec import raknet_packet_codec, raknet_frame_codec
from pyminehub.raknet.frame import Reliability
from pyminehub.raknet.handler import SessionNotFound, RakNetProtocol, GameDataHandler
from pyminehub.raknet.packet import RakNetPacketType, RakNetPacket, raknet_packet_factory
from pyminehub.raknet.session import Session
from pyminehub.value import LogString

_logger = getLogger(__name__)


class _RakNetProtocolImpl(asyncio.DatagramProtocol, RakNetProtocol):

    def __init__(self, loop: asyncio.events.AbstractEventLoop, handler: GameDataHandler) -> None:
        handler.register_protocol(self)
        self._loop = loop
        self._handler = handler
        self._sessions = {}  # TODO session timeout
        self._guid = get_value(ConfigKey.SERVER_GUID)
        self.server_id = 'MCPE;PyMineHub Server;160;1.2.7;0;20;{};{};{};'.format(
            get_value(ConfigKey.SERVER_GUID),
            get_value(ConfigKey.WORLD_NAME),
            get_value(ConfigKey.GAME_MODE).title()
        )
        self._update_task = self._start_loop_to_update(loop)

    def _start_loop_to_update(self, loop: asyncio.AbstractEventLoop) -> asyncio.Task:
        async def loop_to_update():
            while True:
                await self._next_moment()
        return asyncio.ensure_future(loop_to_update(), loop=loop)

    def terminate(self) -> None:
        self._update_task.cancel()
        for session in self._sessions.values():
            session.close()

    def connection_made(self, transport: asyncio.transports.DatagramTransport) -> None:
        # noinspection PyAttributeOutsideInit
        self._transport = transport

    def datagram_received(self, data: bytes, addr: Address) -> None:
        _logger.debug('%s > %s', addr, data.hex())
        packet = raknet_packet_codec.decode(data)
        _logger.debug('> %s', LogString(packet))
        try:
            getattr(self, '_process_' + packet.type.name.lower())(packet, addr)
        except SessionNotFound:
            _logger.info('%s session is not found.', addr)
            self._remove_session(addr)

    def connection_lost(self, exc: Exception) -> None:
        _logger.exception('RakNet connection lost', exc_info=exc)
        self._loop.stop()

    def game_data_received(self, data: bytes, addr: Address, reliability: Reliability) -> None:
        session = self._get_session(addr)
        session.send_frame(data, reliability)

    def send_to_client(self, packet: RakNetPacket, addr: Address) -> None:
        _logger.debug('< %s', LogString(packet))
        data = raknet_packet_codec.encode(packet)
        _logger.debug('%s < %s', addr, data.hex())
        self._transport.sendto(data, addr)

    async def _next_moment(self) -> None:
        try:
            await self._handler.update()
        except SessionNotFound as exc:
            if exc.addr is not None:
                _logger.info('%s session is not found.', exc.addr)
                self._remove_session(exc.addr)

    def _remove_session(self, addr: Address) -> None:
        if addr in self._sessions:
            self._sessions[addr].close()
            del self._sessions[addr]

    def _get_session(self, addr: Address) -> Session:
        try:
            return self._sessions[addr]
        except KeyError:
            raise SessionNotFound(addr)

    def _process_unconnected_ping(self, packet: RakNetPacket, addr: Address) -> None:
        res_packet = raknet_packet_factory.create(
            RakNetPacketType.UNCONNECTED_PONG, packet.time_since_start, self._guid, True, self.server_id)
        self.send_to_client(res_packet, addr)

    def _process_open_connection_request1(self, packet: RakNetPacket, addr: Address) -> None:
        res_packet = raknet_packet_factory.create(
            RakNetPacketType.OPEN_CONNECTION_REPLY1, True, self._guid, False, packet.mtu_size)
        self.send_to_client(res_packet, addr)

    def _process_open_connection_request2(self, packet: RakNetPacket, addr: Address) -> None:
        res_packet = raknet_packet_factory.create(
            RakNetPacketType.OPEN_CONNECTION_REPLY2, True, self._guid, to_packet_format(addr), packet.mtu_size, False)
        self.send_to_client(res_packet, addr)
        self._sessions[addr] = Session(
            self._loop, packet.mtu_size,
            lambda _data: self._handler.data_received(_data, addr),
            lambda _packet: self.send_to_client(_packet, addr))

    def _process_frame_set(self, packet: RakNetPacket, addr: Address) -> None:
        session = self._get_session(addr)
        context = CompositeCodecContext()
        frames = []
        length = 0
        while length < len(packet.payload):
            payload = packet.payload[length:]
            frames.append(raknet_frame_codec.decode(payload, context))
            length += context.length
            context.clear()
        session.frame_received(packet.packet_sequence_num, frames)

    def _process_frame_set_4(self, packet: RakNetPacket, addr: Address) -> None:
        self._process_frame_set(packet, addr)

    def _process_frame_set_8(self, packet: RakNetPacket, addr: Address) -> None:
        self._process_frame_set(packet, addr)

    def _process_frame_set_c(self, packet: RakNetPacket, addr: Address) -> None:
        self._process_frame_set(packet, addr)

    def _process_nck(self, packet: RakNetPacket, addr: Address) -> None:
        session = self._get_session(addr)
        session.nck_received(packet)

    def _process_ack(self, packet: RakNetPacket, addr: Address) -> None:
        session = self._get_session(addr)
        session.ack_received(packet)


def run(loop: asyncio.AbstractEventLoop, handler: GameDataHandler) -> asyncio.Transport:
    server_address = (get_unspecified_address(), get_value(ConfigKey.SERVER_PORT))
    listen = loop.create_datagram_endpoint(
        lambda: _RakNetProtocolImpl(loop, handler), local_addr=server_address)
    transport, protocol = loop.run_until_complete(listen)  # non-blocking
    try:
        loop.run_forever()  # blocking
    except KeyboardInterrupt:
        pass
    finally:
        handler.terminate()
        protocol.terminate()
        pending = asyncio.Task.all_tasks()
        try:
            loop.run_until_complete(asyncio.gather(*pending))
        except asyncio.CancelledError:
            pass
    return transport


if __name__ == '__main__':
    class MockHandler(GameDataHandler):

        def data_received(self, data: bytes, addr: Address) -> None:
            print('{} {}'.format(addr, data.hex()))

        async def update(self) -> None:
            pass

        def terminate(self) -> None:
            pass

    import logging
    logging.basicConfig(level=logging.DEBUG)
    _loop = asyncio.get_event_loop()
    _transport = run(_loop, MockHandler())
    _transport.close()
    _loop.close()
