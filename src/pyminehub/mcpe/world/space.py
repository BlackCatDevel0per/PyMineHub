from typing import Dict, List, Optional, Tuple

from pyminehub.mcpe.chunk import Chunk
from pyminehub.mcpe.const import BlockType, ItemType
from pyminehub.mcpe.geometry import Vector3, ChunkPositionWithDistance, ChunkPosition, to_local_position
from pyminehub.mcpe.value import Item
from pyminehub.mcpe.world.database import DataBase
from pyminehub.mcpe.world.generator import SpaceGenerator


class Space:

    def __init__(self, generator: SpaceGenerator, db: DataBase) -> None:
        self._db = db
        self._generator = generator
        self._size = Vector3(32, 32, 32)
        self._cache = {}  # type: Dict[ChunkPosition, Chunk]

    def init_space(self):
        self._generator.generate_space(self._db, self._size.x, self._size.z)

    def get_chunk(self, request: ChunkPositionWithDistance) -> Chunk:
        if request.position in self._cache:
            return self._cache[request.position]
        chunk = self._generator.generate_chunk(request)
        # TODO save when cache is full
        self._cache[request.position] = chunk
        return chunk

    def _to_local(self, position: Vector3) -> Tuple[Chunk, Vector3]:
        chunk_position = ChunkPosition.at(position)
        chunk = self.get_chunk(ChunkPositionWithDistance(0, chunk_position))
        position_in_chunk = to_local_position(position)
        return chunk, position_in_chunk

    def get_height(self, position: Vector3) -> int:
        chunk, position_in_chunk = self._to_local(position)
        return chunk.get_height(position_in_chunk.x, position_in_chunk.z)

    def break_block(self, position: Vector3[int]) -> Optional[List[Item]]:
        """
        :param position: to break
        :return: None if it can't be broken, or spawned item list if can be broken
        """
        chunk, position_in_chunk = self._to_local(position)
        block_type, block_data = chunk.get_block(position_in_chunk, with_data=True)
        if block_type in (BlockType.AIR, BlockType.BEDROCK):
            return None
        chunk.set_block(position_in_chunk, BlockType.AIR, 0)
        # TODO save chunk
        return [Item(ItemType.DIRT, 1, b'', '', '')]  # TODO change

    def put_block(self, position: Vector3[int], block_type: BlockType) -> None:
        chunk, position_in_chunk = self._to_local(position)
        chunk.set_block(position_in_chunk, block_type)
