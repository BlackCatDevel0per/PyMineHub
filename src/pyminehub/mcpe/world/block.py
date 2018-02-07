from typing import List, Optional, FrozenSet, NamedTuple, Sequence, Tuple

from pyminehub.mcpe.const import BlockType, ItemType
from pyminehub.mcpe.geometry import Vector3, Face
from pyminehub.mcpe.value import Item, Block

__all__ = [
    'FunctionalBlock',
    'PlacedBlock'
]

PlacedBlock = NamedTuple('PlacedBlock', [
    ('position', Vector3[int]),
    ('block', Block)
])

_Connector = FrozenSet[Face]

_CONNECTOR_NONE = frozenset()
_CONNECTOR_BOTTOM = frozenset([Face.BOTTOM])
_CONNECTOR_TOP = frozenset([Face.TOP])
_CONNECTOR_SOUTH = frozenset([Face.SOUTH])
_CONNECTOR_NORTH = frozenset([Face.NORTH])
_CONNECTOR_EAST = frozenset([Face.EAST])
_CONNECTOR_WEST = frozenset([Face.WEST])
_CONNECTOR_SIDE = frozenset([Face.SOUTH, Face.NORTH, Face.EAST, Face.WEST])
_CONNECTOR_ALL = frozenset([Face.BOTTOM, Face.TOP, Face.SOUTH, Face.NORTH, Face.EAST, Face.WEST])


class _BlockSpec:

    def __init__(
            self,
            item_type: Optional[ItemType],
            max_layer_num: int=1,
            can_be_broken: bool=True,
            can_be_attached_on_ground: bool=False,
            is_switchable: bool=False
    ) -> None:
        self._item_type = item_type
        self._max_layer_num = max_layer_num
        self._can_be_broken = can_be_broken
        self._can_be_attached_on_ground = can_be_attached_on_ground
        self._is_switchable = is_switchable

    @property
    def item_type(self) -> Optional[ItemType]:
        return self._item_type

    @property
    def has_layer(self) -> bool:
        return self._max_layer_num > 1

    @property
    def max_layer_num(self) -> int:
        return self._max_layer_num

    @property
    def can_be_broken(self) -> bool:
        return self._can_be_broken

    @property
    def can_be_attached_on_ground(self) -> bool:
        return self._can_be_attached_on_ground

    @property
    def is_switchable(self) -> bool:
        return self._is_switchable

    def get_link_target(self, block: Block) -> Tuple[Vector3[int], ...]:
        return ()

    def get_break_target(self, block: Block) -> Tuple[Vector3[int], ...]:
        return Vector3(0, 0, 0),

    def to_item(self, block_data: int) -> List[Item]:
        return [Item.create(self.item_type, 1, block_data)] if self.item_type is not None else []

    def stack_layer(self, base_block: Block, stacked_block: Block, face: Face) -> Optional[Block]:
        assert self.has_layer > 1
        return None

    def get_switch_position(self, block: Block) -> Vector3[int]:
        return Vector3(0, 0, 0)

    def switch(self, block: Block) -> Block:
        assert self.is_switchable
        return block

    def get_additional_blocks(self, block: Block, linked_blocks: Sequence[Block]) -> Tuple[PlacedBlock, ...]:
        return PlacedBlock(Vector3(0, 0, 0), block),

    def female_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_ALL

    def male_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_ALL

    def can_be_attached_on(self, block: Block) -> bool:
        return True


class _AirBlockSpec(_BlockSpec):

    def __init__(self) -> None:
        super().__init__(None, can_be_broken=False)

    def female_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_NONE

    def male_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_NONE


class _ToExtendUpwardBlockSpec(_BlockSpec):

    def female_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_NONE

    def male_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_BOTTOM


class _SlabBlockSpec(_BlockSpec):

    _SLAB_TYPE_MASK = 0b111
    _IS_UPPER_MASK = 0b1000

    def __init__(self, item_type: Optional[ItemType], full_stacked_block_type: BlockType) -> None:
        super().__init__(item_type, 2)
        self._full_stacked_block_type = full_stacked_block_type

    def stack_layer(self, base_block: Block, stacked_block: Block, face: Face) -> Optional[Block]:
        """
        >>> spec = _SlabBlockSpec(None, BlockType.DOUBLE_WOODEN_SLAB)
        >>> block_type = BlockType.WOODEN_SLAB
        >>> spec.stack_layer(Block.create(block_type, 0), Block.create(block_type, 8), Face.TOP)
        Block(type=<BlockType.DOUBLE_WOODEN_SLAB: 157>, aux_value=0)
        >>> spec.stack_layer(Block.create(block_type, 8), Block.create(block_type, 0), Face.BOTTOM)
        Block(type=<BlockType.DOUBLE_WOODEN_SLAB: 157>, aux_value=0)
        >>> spec.stack_layer(Block.create(block_type, 8), Block.create(block_type, 0), Face.TOP)
        >>> spec.stack_layer(Block.create(block_type, 0), Block.create(block_type, 8), Face.BOTTOM)
        >>> spec.stack_layer(Block.create(block_type, 0, neighbors=True), Block.create(block_type, 8), Face.TOP)
        Block(type=<BlockType.DOUBLE_WOODEN_SLAB: 157>, aux_value=0)
        >>> spec.stack_layer(Block.create(block_type, 0), Block.create(block_type, 8, neighbors=True), Face.TOP)
        Block(type=<BlockType.DOUBLE_WOODEN_SLAB: 157>, aux_value=16)
        >>> spec.stack_layer(\\
        ...     Block.create(block_type, 0, neighbors=True), Block.create(block_type, 8, neighbors=False), Face.TOP)
        Block(type=<BlockType.DOUBLE_WOODEN_SLAB: 157>, aux_value=0)
        """
        slab_type = stacked_block.data & self._SLAB_TYPE_MASK
        if slab_type != base_block.data & self._SLAB_TYPE_MASK:
            return base_block
        is_upper = stacked_block.data & self._IS_UPPER_MASK
        if is_upper != base_block.data & self._IS_UPPER_MASK:
            if (face is Face.BOTTOM and is_upper) or (face is Face.TOP and not is_upper):
                return None
            return Block.create(self._full_stacked_block_type, slab_type, **stacked_block.flags)
        return None

    def female_connector(self, block: Block) -> _Connector:
        if block.data & self._IS_UPPER_MASK:
            return _CONNECTOR_ALL - _CONNECTOR_BOTTOM
        else:
            return _CONNECTOR_ALL - _CONNECTOR_TOP

    def male_connector(self, block: Block):
        if block.data & self._IS_UPPER_MASK:
            return _CONNECTOR_ALL - _CONNECTOR_BOTTOM
        else:
            return _CONNECTOR_ALL - _CONNECTOR_TOP


class _SnowLayerBlockSpec(_ToExtendUpwardBlockSpec):

    def __init__(self) -> None:
        super().__init__(None, max_layer_num=8, can_be_attached_on_ground=True)

    def stack_layer(self, base_block: Block, stacked_block: Block, face: Face) -> Optional[Block]:
        """
        >>> spec = _SnowLayerBlockSpec()
        >>> block_type = BlockType.SNOW_LAYER
        >>> spec.stack_layer(Block.create(block_type, 0), Block.create(block_type, 0), Face.TOP)
        Block(type=<BlockType.SNOW_LAYER: 78>, aux_value=1)
        >>> spec.stack_layer(Block.create(block_type, 1), Block.create(block_type, 0), Face.TOP)
        Block(type=<BlockType.SNOW_LAYER: 78>, aux_value=2)
        >>> spec.stack_layer(Block.create(block_type, 5), Block.create(block_type, 0), Face.TOP)
        Block(type=<BlockType.SNOW_LAYER: 78>, aux_value=6)
        >>> spec.stack_layer(Block.create(block_type, 6), Block.create(block_type, 0), Face.TOP)
        Block(type=<BlockType.SNOW: 80>, aux_value=0)
        """
        layer_index = base_block.data + 1
        if layer_index != self.max_layer_num - 1:
            return Block.create(BlockType.SNOW_LAYER, layer_index, **stacked_block.flags)
        else:
            return Block.create(BlockType.SNOW, 0, **stacked_block.flags)


class _LadderBlockSpec(_BlockSpec):

    _CAN_BE_ATTACHED = (
        BlockType.PLANKS,

        BlockType.BRICK_BLOCK,
        BlockType.STONE_BRICK,
        BlockType.END_BRICK,
        BlockType.PRISMARINE,
        BlockType.NETHER_BRICK_BLOCK,
        BlockType.RED_NETHER_BRICK,
        BlockType.COBBLESTONE,
        BlockType.MOSSY_COBBLESTONE,

        BlockType.SANDSTONE,
        BlockType.RED_SANDSTONE,
        BlockType.COAL_BLOCK,
        BlockType.REDSTONE_BLOCK,
        BlockType.GOLD_BLOCK,
        BlockType.IRON_BLOCK,
        BlockType.EMERALD_BLOCK,
        BlockType.DIAMOND_BLOCK,
        BlockType.LAPIS_BLOCK,
        BlockType.QUARTZ_BLOCK,
        BlockType.HAY_BLOCK,
        BlockType.BONE_BLOCK,
        BlockType.NETHER_WART_BLOCK,
        BlockType.WOOL,

        BlockType.CONCRETE_POWDER,
        BlockType.CONCRETE,
        BlockType.CLAY,
        BlockType.HARDENED_CLAY,
        BlockType.STAINED_HARDENED_CLAY,
        BlockType.WHITE_GLAZED_TERRACOTTA,
        BlockType.SILVER_GLAZED_TERRACOTTA,
        BlockType.GRAY_GLAZED_TERRACOTTA,
        BlockType.BLACK_GLAZED_TERRACOTTA,
        BlockType.BROWN_GLAZED_TERRACOTTA,
        BlockType.RED_GLAZED_TERRACOTTA,
        BlockType.ORANGE_GLAZED_TERRACOTTA,
        BlockType.YELLOW_GLAZED_TERRACOTTA,
        BlockType.LIME_GLAZED_TERRACOTTA,
        BlockType.GREEN_GLAZED_TERRACOTTA,
        BlockType.CYAN_GLAZED_TERRACOTTA,
        BlockType.LIGHT_BLUE_GLAZED_TERRACOTTA,
        BlockType.BLUE_GLAZED_TERRACOTTA,
        BlockType.PURPLE_GLAZED_TERRACOTTA,
        BlockType.MAGENTA_GLAZED_TERRACOTTA,
        BlockType.PINK_GLAZED_TERRACOTTA,
        BlockType.PURPUR_BLOCK,

        BlockType.DOUBLE_STONE_SLAB,
        BlockType.DOUBLE_WOODEN_SLAB,
        BlockType.DOUBLE_STONE_SLAB2,

        BlockType.DIRT,
        BlockType.PODZOL,
        BlockType.MYCELIUM,
        BlockType.STONE,
        BlockType.IRON_ORE,
        BlockType.GOLD_ORE,
        BlockType.DIAMOND_ORE,
        BlockType.LAPIS_ORE,
        BlockType.REDSTONE_ORE,
        BlockType.COAL_ORE,
        BlockType.EMERALD_ORE,
        BlockType.QUARTZ_ORE,
        BlockType.GRAVEL,
        BlockType.SAND,
        BlockType.LOG,
        BlockType.LOG2,

        BlockType.MELON_BLOCK,
        BlockType.PUMPKIN,
        BlockType.LIT_PUMPKIN,

        BlockType.SNOW,
        BlockType.PACKED_ICE,

        BlockType.BROWN_MUSHROOM_BLOCK,
        BlockType.RED_MUSHROOM_BLOCK,

        BlockType.MOB_SPAWNER,

        BlockType.OBSIDIAN,
        BlockType.BEDROCK,
        BlockType.SOUL_SAND,
        BlockType.NETHERRACK,
        BlockType.MAGMA,
        BlockType.END_STONE,
        BlockType.SPONGE,

        BlockType.REDSTONE_LAMP,
        BlockType.OBSERVER,
        BlockType.PISTON,
        BlockType.STICKY_PISTON,
    )

    _CONNECTOR = {
        2: _CONNECTOR_NORTH,
        3: _CONNECTOR_SOUTH,
        4: _CONNECTOR_WEST,
        5: _CONNECTOR_EAST
    }

    def __init__(self) -> None:
        super().__init__(ItemType.LADDER)

    def female_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_NONE

    def male_connector(self, block: Block) -> _Connector:
        return self._CONNECTOR[block.data]

    def can_be_attached_on(self, block: Block) -> bool:
        return block.type in self._CAN_BE_ATTACHED


class _FenceGateBlockSpec(_ToExtendUpwardBlockSpec):

    _DOES_OPEN_MASK = 0b100

    def __init__(self, item_type: Optional[ItemType]) -> None:
        super().__init__(item_type, can_be_attached_on_ground=True, is_switchable=True)

    def switch(self, block: Block) -> Block:
        return block.copy(data=block.data ^ self._DOES_OPEN_MASK)


class _TrapDoorBlockSpec(_BlockSpec):

    _DOES_OPEN_MASK = 0b1000

    def __init__(self, item_type: Optional[ItemType]) -> None:
        super().__init__(item_type, is_switchable=True)

    def switch(self, block: Block) -> Block:
        return block.copy(data=block.data ^ self._DOES_OPEN_MASK)

    def female_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_NONE

    def male_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_ALL


class _CarpetBlockSpec(_ToExtendUpwardBlockSpec):

    def __init__(self) -> None:
        super().__init__(ItemType.CARPET, can_be_attached_on_ground=True)


class _DoublePlantBlockSpec(_ToExtendUpwardBlockSpec):

    _IS_UPPER_MASK = 0b1000

    def _is_upper(self, block: Block) -> bool:
        return bool(block.data & self._IS_UPPER_MASK)

    def get_break_target(self, block: Block) -> Tuple[Vector3[int], ...]:
        if self._is_upper(block):
            return Vector3(0, 0, 0),
        else:
            return Vector3(0, 1, 0), Vector3(0, 0, 0)

    def get_additional_blocks(self, block: Block, linked_blocks: Sequence[Block]) -> Tuple[PlacedBlock, ...]:
        return PlacedBlock(Vector3(0, 0, 0), block), PlacedBlock(Vector3(0, 1, 0), block.copy(data=self._IS_UPPER_MASK))


class _DoorBlockSpec(_ToExtendUpwardBlockSpec):

    # set to the upper part
    _IS_UPPER_MASK = 0b1000
    _IS_RIGHT_SIDE_MASK = 0b1

    # set to the lower part
    _DOES_OPEN_MASK = 0b100
    _FACE_MASK = 0b11

    _LEFT_SIDE = {
        0: Vector3(0, 0, -1),
        1: Vector3(1, 0, 0),
        2: Vector3(0, 0, 1),
        3: Vector3(-1, 0, 0)
    }

    _BREAK_ORDER = (Vector3(0, 1, 0), Vector3(0, 0, 0))

    def __init__(self, item_type: Optional[ItemType]) -> None:
        super().__init__(item_type, is_switchable=True)

    def _get_face(self, block: Block) -> int:
        return block.data & self._FACE_MASK

    def _is_upper_part(self, block: Block) -> bool:
        return bool(block.data & self._IS_UPPER_MASK)

    def _is_right_side(self, block: Block) -> bool:
        assert self._is_upper_part(block)
        return bool(block.data & self._IS_RIGHT_SIDE_MASK)

    def get_link_target(self, block: Block) -> Tuple[Vector3[int], ...]:
        """
        >>> spec = _DoorBlockSpec(None)
        >>> spec.get_link_target(Block.create(BlockType.WOODEN_DOOR_BLOCK, 0))
        (Vector3(x=0, y=0, z=-1), Vector3(x=0, y=1, z=-1))
        >>> spec.get_link_target(Block.create(BlockType.WOODEN_DOOR_BLOCK, 1))
        (Vector3(x=1, y=0, z=0), Vector3(x=1, y=1, z=0))
        >>> spec.get_link_target(Block.create(BlockType.WOODEN_DOOR_BLOCK, 2))
        (Vector3(x=0, y=0, z=1), Vector3(x=0, y=1, z=1))
        >>> spec.get_link_target(Block.create(BlockType.WOODEN_DOOR_BLOCK, 3))
        (Vector3(x=-1, y=0, z=0), Vector3(x=-1, y=1, z=0))
        """
        assert not self._is_upper_part(block)
        left_side = self._LEFT_SIDE[self._get_face(block)]
        return left_side, left_side + (0, 1, 0)

    def get_break_target(self, block: Block) -> Tuple[Vector3[int], ...]:
        dy = -1 if self._is_upper_part(block) else 0
        return tuple(p + (0, dy, 0) for p in self._BREAK_ORDER)

    def get_switch_position(self, block: Block) -> Vector3[int]:
        dy = -1 if self._is_upper_part(block) else 0
        return Vector3(0, dy, 0)

    def switch(self, block: Block) -> Block:
        return block.copy(data=block.data ^ self._DOES_OPEN_MASK)

    def get_additional_blocks(self, block: Block, linked_blocks: Sequence[Block]) -> Tuple[PlacedBlock, ...]:
        assert len(linked_blocks) == 2
        left_side_lower_block, left_side_upper_block = linked_blocks
        right_side_mask = 0
        if left_side_lower_block.type == block.type and self._get_face(left_side_lower_block) == self._get_face(block):
            if not self._is_right_side(left_side_upper_block):
                right_side_mask = self._IS_RIGHT_SIDE_MASK
        data = self._IS_UPPER_MASK | right_side_mask
        return PlacedBlock(Vector3(0, 0, 0), block), PlacedBlock(Vector3(0, 1, 0), block.copy(data=data))


class _EndRodBlockSpec(_BlockSpec):

    _BASE_SIDE = {
        0: Vector3(0, 1, 0),
        1: Vector3(0, -1, 0),
        2: Vector3(0, 0, -1),
        3: Vector3(0, 0, 1),
        4: Vector3(-1, 0, 0),
        5: Vector3(1, 0, 0)
    }

    def __init__(self) -> None:
        super().__init__(ItemType.END_ROD)

    def get_link_target(self, block: Block) -> Tuple[Vector3[int], ...]:
        return self._BASE_SIDE[block.data],

    def get_additional_blocks(self, block: Block, linked_blocks: Sequence[Block]) -> Tuple[PlacedBlock, ...]:
        assert len(linked_blocks) == 1
        base_side_block = linked_blocks[0]
        if base_side_block.type == block.type and base_side_block.data == block.data:
            block = block.copy(data=block.data ^ 1)
        return PlacedBlock(Vector3(0, 0, 0), block),


class _ToggleBlockSpec(_BlockSpec):

    _TOGGLE_MASK = 0b1000

    def __init__(self, item_type: Optional[ItemType]) -> None:
        super().__init__(item_type, is_switchable=True)

    def switch(self, block: Block) -> Block:
        return block.copy(data=block.data ^ self._TOGGLE_MASK)

    def female_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_NONE

    def male_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_ALL


class _TripwireHookBlockSpec(_BlockSpec):

    def female_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_NONE

    def male_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_SIDE


class _DaylightDetectorBlockSpec(_BlockSpec):

    def __init__(self, item_type: Optional[ItemType]) -> None:
        super().__init__(item_type, is_switchable=True)

    def switch(self, block: Block) -> Block:
        block_type = BlockType.DAYLIGHT_DETECTOR_INVERTED \
            if block.type is BlockType.DAYLIGHT_DETECTOR else BlockType.DAYLIGHT_DETECTOR
        return block.copy(block_type=block_type)

    def female_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_NONE

    def male_connector(self, block: Block) -> _Connector:
        return _CONNECTOR_BOTTOM


_block_specs = {
    BlockType.AIR: _AirBlockSpec(),
    BlockType.BEDROCK: _BlockSpec(None, can_be_broken=False),
    BlockType.GRASS: _BlockSpec(ItemType.DIRT),
    BlockType.STONE_SLAB: _SlabBlockSpec(ItemType.STONE_SLAB, BlockType.DOUBLE_STONE_SLAB),
    BlockType.WOODEN_SLAB: _SlabBlockSpec(ItemType.WOODEN_SLAB, BlockType.DOUBLE_WOODEN_SLAB),
    BlockType.STONE_SLAB2: _SlabBlockSpec(ItemType.STONE_SLAB2, BlockType.DOUBLE_STONE_SLAB2),
    BlockType.SNOW_LAYER: _SnowLayerBlockSpec(),
    BlockType.LADDER: _LadderBlockSpec(),
    BlockType.TRAPDOOR: _TrapDoorBlockSpec(ItemType.TRAPDOOR),
    BlockType.IRON_TRAPDOOR: _TrapDoorBlockSpec(ItemType.IRON_TRAPDOOR),
    BlockType.CARPET: _CarpetBlockSpec(),
    BlockType.DOUBLE_PLANT: _DoublePlantBlockSpec(ItemType.DOUBLE_PLANT),
    BlockType.CAKE_BLOCK: _ToExtendUpwardBlockSpec(ItemType.CAKE),
    BlockType.FLOWER_POT_BLOCK: _ToExtendUpwardBlockSpec(ItemType.FLOWER_POT, can_be_attached_on_ground=True),
    BlockType.END_ROD: _EndRodBlockSpec(),
    BlockType.LEVER: _ToggleBlockSpec(ItemType.LEVER),
    BlockType.WOODEN_BUTTON: _ToggleBlockSpec(ItemType.WOODEN_BUTTON),
    BlockType.STONE_BUTTON: _ToggleBlockSpec(ItemType.STONE_BUTTON),
    BlockType.TRIPWIRE_HOOK: _TripwireHookBlockSpec(ItemType.TRIPWIRE_HOOK),
    BlockType.DAYLIGHT_DETECTOR: _DaylightDetectorBlockSpec(ItemType.DAYLIGHT_DETECTOR),
    BlockType.DAYLIGHT_DETECTOR_INVERTED: _DaylightDetectorBlockSpec(ItemType.DAYLIGHT_DETECTOR),
}


_blocks = [
    BlockType.PLANKS,

    BlockType.COBBLESTONE_WALL,

    BlockType.FENCE,
    BlockType.NETHER_BRICK_FENCE,

    BlockType.STONE_STAIRS,
    BlockType.OAK_STAIRS,
    BlockType.SPRUCE_STAIRS,
    BlockType.BIRCH_STAIRS,
    BlockType.JUNGLE_STAIRS,
    BlockType.ACACIA_STAIRS,
    BlockType.DARK_OAK_STAIRS,
    BlockType.BRICK_STAIRS,
    BlockType.STONE_BRICK_STAIRS,
    BlockType.NETHER_BRICK_STAIRS,
    BlockType.SANDSTONE_STAIRS,
    BlockType.RED_SANDSTONE_STAIRS,
    BlockType.QUARTZ_STAIRS,
    BlockType.PURPUR_STAIRS,

    BlockType.IRON_BARS,

    BlockType.GLASS,
    BlockType.STAINED_GLASS,
    BlockType.GLASS_PANE,
    BlockType.STAINED_GLASS_PANE,

    BlockType.BRICK_BLOCK,
    BlockType.STONE_BRICK,
    BlockType.END_BRICK,
    BlockType.PRISMARINE,
    BlockType.NETHER_BRICK_BLOCK,
    BlockType.RED_NETHER_BRICK,
    BlockType.COBBLESTONE,
    BlockType.MOSSY_COBBLESTONE,

    BlockType.SANDSTONE,
    BlockType.RED_SANDSTONE,
    BlockType.COAL_BLOCK,
    BlockType.REDSTONE_BLOCK,
    BlockType.GOLD_BLOCK,
    BlockType.IRON_BLOCK,
    BlockType.EMERALD_BLOCK,
    BlockType.DIAMOND_BLOCK,
    BlockType.LAPIS_BLOCK,
    BlockType.QUARTZ_BLOCK,
    BlockType.HAY_BLOCK,
    BlockType.BONE_BLOCK,
    BlockType.NETHER_WART_BLOCK,
    BlockType.WOOL,

    BlockType.CONCRETE_POWDER,
    BlockType.CONCRETE,
    BlockType.CLAY,
    BlockType.HARDENED_CLAY,
    BlockType.STAINED_HARDENED_CLAY,
    BlockType.WHITE_GLAZED_TERRACOTTA,
    BlockType.SILVER_GLAZED_TERRACOTTA,
    BlockType.GRAY_GLAZED_TERRACOTTA,
    BlockType.BLACK_GLAZED_TERRACOTTA,
    BlockType.BROWN_GLAZED_TERRACOTTA,
    BlockType.RED_GLAZED_TERRACOTTA,
    BlockType.ORANGE_GLAZED_TERRACOTTA,
    BlockType.YELLOW_GLAZED_TERRACOTTA,
    BlockType.LIME_GLAZED_TERRACOTTA,
    BlockType.GREEN_GLAZED_TERRACOTTA,
    BlockType.CYAN_GLAZED_TERRACOTTA,
    BlockType.LIGHT_BLUE_GLAZED_TERRACOTTA,
    BlockType.BLUE_GLAZED_TERRACOTTA,
    BlockType.PURPLE_GLAZED_TERRACOTTA,
    BlockType.MAGENTA_GLAZED_TERRACOTTA,
    BlockType.PINK_GLAZED_TERRACOTTA,
    BlockType.PURPUR_BLOCK,
    BlockType.DIRT,
    BlockType.PODZOL,
    BlockType.MYCELIUM,
    BlockType.STONE,
    BlockType.IRON_ORE,
    BlockType.GOLD_ORE,
    BlockType.DIAMOND_ORE,
    BlockType.LAPIS_ORE,
    BlockType.REDSTONE_ORE,
    BlockType.COAL_ORE,
    BlockType.EMERALD_ORE,
    BlockType.QUARTZ_ORE,
    BlockType.GRAVEL,
    BlockType.SAND,
    BlockType.CACTUS,
    BlockType.LOG,
    BlockType.LOG2,
    BlockType.LEAVES,
    BlockType.LEAVES2,

    BlockType.MELON_BLOCK,
    BlockType.PUMPKIN,
    BlockType.LIT_PUMPKIN,

    BlockType.VINE,

    BlockType.SNOW,
    BlockType.ICE,
    BlockType.PACKED_ICE,

    BlockType.MOB_SPAWNER,

    BlockType.OBSIDIAN,
    BlockType.SOUL_SAND,
    BlockType.NETHERRACK,
    BlockType.MAGMA,
    BlockType.END_STONE,
    BlockType.SPONGE,

    BlockType.WEB,

    BlockType.TORCH,
    BlockType.REDSTONE_TORCH,
    BlockType.REDSTONE_LAMP,
    BlockType.SEA_LANTERN,

    BlockType.GLOWSTONE,

    BlockType.CHEST,
    BlockType.TRAPPED_CHEST,
    BlockType.ENDER_CHEST,
    BlockType.BOOKSHELF,

    BlockType.END_PORTAL_FRAME,

    BlockType.GRASS_PATH,

    BlockType.RAIL,
    BlockType.GOLDEN_RAIL,
    BlockType.DETECTOR_RAIL,
    BlockType.ACTIVATOR_RAIL,

    BlockType.TNT,

    BlockType.DOUBLE_STONE_SLAB,
    BlockType.DOUBLE_WOODEN_SLAB,
    BlockType.DOUBLE_STONE_SLAB2,

    BlockType.FLOWING_WATER,
    BlockType.FLOWING_LAVA,
]

_fence_gate_blocks = [
    BlockType.FENCE_GATE,
    BlockType.SPRUCE_FENCE_GATE,
    BlockType.BIRCH_FENCE_GATE,
    BlockType.JUNGLE_FENCE_GATE,
    BlockType.ACACIA_FENCE_GATE,
    BlockType.DARK_OAK_FENCE_GATE,
]

_plant_blocks = [
    BlockType.SAPLING,
    BlockType.TALLGRASS,
    BlockType.YELLOW_FLOWER,
    BlockType.FLOWER,
    BlockType.LILY_PAD,
    BlockType.DEAD_BUSH,
    BlockType.BROWN_MUSHROOM,
    BlockType.RED_MUSHROOM,
]

_door_blocks = [
    (ItemType.WOODEN_DOOR, BlockType.WOODEN_DOOR_BLOCK),
    (ItemType.IRON_DOOR, BlockType.IRON_DOOR_BLOCK),
    (ItemType.SPRUCE_DOOR, BlockType.SPRUCE_DOOR_BLOCK),
    (ItemType.BIRCH_DOOR, BlockType.BIRCH_DOOR_BLOCK),
    (ItemType.JUNGLE_DOOR, BlockType.JUNGLE_DOOR_BLOCK),
    (ItemType.ACACIA_DOOR, BlockType.ACACIA_DOOR_BLOCK),
    (ItemType.DARK_OAK_DOOR, BlockType.DARK_OAK_DOOR_BLOCK),
]

_tool_blocks = [
    BlockType.CRAFTING_TABLE,
    BlockType.FURNACE,
    BlockType.ANVIL,
    BlockType.ENCHANTING_TABLE,
    BlockType.NOTEBLOCK,
    BlockType.STONECUTTER,
]

_pressure_plate_blocks = [
    BlockType.WOODEN_PRESSURE_PLATE,
    BlockType.STONE_PRESSURE_PLATE,
    BlockType.LIGHT_WEIGHTED_PRESSURE_PLATE,
    BlockType.HEAVY_WEIGHTED_PRESSURE_PLATE,
]


for _block_type in _blocks:
    _block_specs[_block_type] = _BlockSpec(ItemType(_block_type.value))

for _block_type in _fence_gate_blocks:
    _block_specs[_block_type] = _FenceGateBlockSpec(ItemType(_block_type.value))

for _block_type in _plant_blocks:
    _block_specs[_block_type] = _ToExtendUpwardBlockSpec(ItemType(_block_type.value))

for _item_type, _block_type in _door_blocks:
    _block_specs[_block_type] = _DoorBlockSpec(_item_type)

for _block_type in _tool_blocks:
    _block_specs[_block_type] = _ToExtendUpwardBlockSpec(ItemType(_block_type.value))

for _block_type in _pressure_plate_blocks:
    _block_specs[_block_type] = _ToExtendUpwardBlockSpec(ItemType(_block_type.value))


class FunctionalBlock:
    """Functional block joins block value and block specification"""

    def __init__(self, block: Block) -> None:
        self._block = block
        self._block_spec = _block_specs[block.type]

    def __str__(self) -> str:
        return str(self._block)

    @property
    def type(self) -> BlockType:
        return self._block.type

    @property
    def value(self) -> Block:
        return self._block

    @property
    def has_layer(self) -> bool:
        return self._block_spec.has_layer

    @property
    def can_be_broken(self) -> bool:
        return self._block_spec.can_be_broken

    @property
    def can_be_attached_on_ground(self) -> bool:
        return self._block_spec.can_be_attached_on_ground

    @property
    def is_switchable(self) -> bool:
        return self._block_spec.is_switchable

    @property
    def switch_position(self) -> Vector3[int]:
        return self._block_spec.get_switch_position(self._block)

    @property
    def link_target(self) -> Tuple[Vector3[int], ...]:
        return self._block_spec.get_link_target(self._block)

    @property
    def break_target(self) -> Tuple[Vector3[int], ...]:
        return self._block_spec.get_break_target(self._block)

    def to_item(self) -> List[Item]:
        return self._block_spec.to_item(self._block.data)

    def stack_on(self, base_block: Block, face: Face) -> Optional[Block]:
        return self._block_spec.stack_layer(base_block, self._block, face)

    def switch(self) -> Block:
        return self._block_spec.switch(self._block)

    def can_be_attached_on(self, base_block: Block, face: Face) -> bool:
        if face.inverse not in self._block_spec.male_connector(self._block):
            return False
        base_block_spec = _block_specs[base_block.type]
        if face not in base_block_spec.female_connector(base_block):
            return False
        return self._block_spec.can_be_attached_on(base_block)

    def get_additional_blocks(self, linked_blocks: Sequence[Block]) -> Tuple[PlacedBlock, ...]:
        return self._block_spec.get_additional_blocks(self._block, linked_blocks)


if __name__ == '__main__':
    import doctest
    doctest_result = doctest.testmod()
