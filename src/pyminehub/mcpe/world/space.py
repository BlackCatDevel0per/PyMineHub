from typing import Dict, List, Optional, Tuple

from pyminehub.mcpe.chunk import Chunk
from pyminehub.mcpe.const import BlockType
from pyminehub.mcpe.datastore import DataStore
from pyminehub.mcpe.geometry import Vector3, ChunkPositionWithDistance, ChunkPosition, to_local_position
from pyminehub.mcpe.value import Item, Block
from pyminehub.mcpe.world.block import get_block_spec
from pyminehub.mcpe.world.generator import SpaceGenerator

__all__ = [
    'BLOCK_AIR',
    'Space'
]


BLOCK_AIR = Block(BlockType.AIR, 0)


class Space:

    def __init__(self, generator: SpaceGenerator, store: DataStore) -> None:
        self._store = store
        self._generator = generator
        self._size = Vector3(32, 32, 32)
        self._cache = {}  # type: Dict[ChunkPosition, Chunk]

    def init_space(self) -> None:
        self._generator.generate_space(self._size.x, self._size.z)

    def save(self) -> None:
        for position, chunk in self._cache.items():
            if chunk.is_updated:
                self._store.save_chunk(position, chunk)
                chunk.is_updated = False

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
        block = chunk.get_block(position_in_chunk)
        if block.type in (BlockType.AIR, BlockType.BEDROCK):
            return None
        chunk.set_block(position_in_chunk, BLOCK_AIR)
        return get_block_spec(block.type).to_item()

    def put_block(self, position: Vector3[int], block: Block) -> None:
        chunk, position_in_chunk = self._to_local(position)
        chunk.set_block(position_in_chunk, block)

    def revise_position(self, position: Vector3[float]) -> Vector3[float]:
        height = self.get_height(position)
        return position.copy(y=height)
