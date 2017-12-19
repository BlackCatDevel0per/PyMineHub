import asyncio
from logging import getLogger, basicConfig

from pyminehub.config import ConfigKey, get_value
from pyminehub.network.address import IP_VERSION, Address, to_packet_format
from pyminehub.network.codec import PacketCodecContext
from pyminehub.raknet.codec import raknet_packet_codec, raknet_frame_codec
from pyminehub.raknet.frame import Reliability
from pyminehub.raknet.packet import RakNetPacketType, RakNetPacket, raknet_packet_factory
from pyminehub.raknet.session import Session

_logger = getLogger(__name__)


class GameDataHandler:

    def register_protocol(self, protocol) -> None:
        # noinspection PyAttributeOutsideInit
        self._protocol = protocol

    def sendto(self, data: bytes, addr: Address, reliability: Reliability) -> None:
        self._protocol.game_data_received(data, addr, reliability)

    def data_received(self, data: bytes, addr: Address) -> None:
        raise NotImplementedError()


class _RakNetServerProtocol(asyncio.DatagramProtocol):

    def __init__(self, loop: asyncio.events.AbstractEventLoop, handler: GameDataHandler) -> None:
        handler.register_protocol(self)
        self._loop = loop
        self._handler = handler
        self._sessions = {}  # TODO session timeout
        self._guid = get_value(ConfigKey.SERVER_GUID)
        self.server_id = 'MCPE;Steve;137;1.2.3;1;5;472877960873915065;testWorld;Survival;'

    def connection_made(self, transport: asyncio.transports.DatagramTransport) -> None:
        # noinspection PyAttributeOutsideInit
        self._transport = transport

    def datagram_received(self, data: bytes, addr: Address) -> None:
        _logger.debug('%s [%d] %s', addr, len(data), data.hex())
        packet = raknet_packet_codec.decode(data)
        _logger.debug('> %s %s', addr, packet)
        getattr(self, '_process_' + RakNetPacketType(packet.id).name.lower())(packet, addr)

    def connection_lost(self, exc: Exception) -> None:
        _logger.exception('RakNet connection lost', exc_info=exc)
        self._loop.stop()

    def game_data_received(self, data: bytes, addr: Address, reliability: Reliability) -> None:
        session = self._sessions[addr]
        session.send_custom_packet(data, reliability)

    def send_to_client(self, packet: RakNetPacket, addr: Address) -> None:
        _logger.debug('< %s %s', addr, packet)
        self._transport.sendto(raknet_packet_codec.encode(packet), addr)

    def send_waiting_packets(self) -> None:
        for addr, session in self._sessions.items():
            session.send_waiting_pacckets()

    def _process_unconnected_ping(self, packet: RakNetPacket, addr: Address) -> None:
        res_packet = raknet_packet_factory.create(
            RakNetPacketType.UNCONNECTED_PONG, packet.time_since_start, self._guid, True, self.server_id)
        self.send_to_client(res_packet, addr)

    def _process_open_connection_request1(self, packet: RakNetPacket, addr: Address) -> None:
        res_packet = raknet_packet_factory.create(
            RakNetPacketType.OPEN_CONNECTION_REPLY1, True, self._guid, False, packet.mtu_size)
        self.send_to_client(res_packet, addr)

    def _process_open_connection_request2(self, packet: RakNetPacket, addr: Address) -> None:
        assert packet.server_address.ip_version == IP_VERSION
        res_packet = raknet_packet_factory.create(
            RakNetPacketType.OPEN_CONNECTION_REPLY2, True, self._guid, to_packet_format(addr), packet.mtu_size, False)
        self.send_to_client(res_packet, addr)
        self._sessions[addr] = Session(
            packet.mtu_size,
            lambda _data: self._handler.data_received(_data, addr),
            lambda _packet: self.send_to_client(_packet, addr))

    def _process_custom_packet(self, packet: RakNetPacket, addr: Address) -> None:
        session = self._sessions[addr]
        context = PacketCodecContext()
        frames = []
        length = 0
        while length < len(packet.payload):
            payload = packet.payload[length:]
            _logger.debug('%s', payload.hex())
            frames.append(raknet_frame_codec.decode(payload, context))
            length += context.length
            context.clear()
        session.frame_received(packet.packet_sequence_num, frames)

    def _process_custom_packet_4(self, packet: RakNetPacket, addr: Address) -> None:
        self._process_custom_packet(packet, addr)

    def _process_custom_packet_c(self, packet: RakNetPacket, addr: Address) -> None:
        self._process_custom_packet(packet, addr)

    def _process_nck(self, packet: RakNetPacket, addr: Address) -> None:
        session = self._sessions[addr]
        session.nck_received(packet)

    def _process_ack(self, packet: RakNetPacket, addr: Address) -> None:
        session = self._sessions[addr]
        session.ack_received(packet)


async def _send(protocol: _RakNetServerProtocol):
    while True:
        await asyncio.sleep(0.1)
        protocol.send_waiting_packets()


def run(handler, log_level=None) -> None:
    not log_level or basicConfig(level=log_level)
    loop = asyncio.get_event_loop()
    listen = loop.create_datagram_endpoint(
        lambda: _RakNetServerProtocol(loop, handler), local_addr=('0.0.0.0', 19132))
    transport, protocol = loop.run_until_complete(listen)
    try:
        loop.run_until_complete(_send(protocol))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        transport.close()
        loop.close()


if __name__ == '__main__':
    import logging

    class MockHandler(GameDataHandler):
        def data_received(self, data: bytes, addr: Address) -> None:
            print('{} {}'.format(addr, data.hex()))

    run(MockHandler(), logging.DEBUG)
