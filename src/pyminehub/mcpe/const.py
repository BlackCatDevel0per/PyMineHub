from enum import Enum


OWN_PLAYER_ENTITY_ID = 1


class PlayStatus(Enum):
    LOGIN_SUCCESS = 0
    LOGIN_FAILED_CLIENT = 1
    LOGIN_FAILED_SERVER = 2
    PLAYER_SPAWN = 3
    LOGIN_FAILED_INVALID_TENANT = 4
    LOGIN_FAILED_VANILLA_EDU = 5
    LOGIN_FAILED_EDU_VANILLA = 6


class ResourcePackStatus(Enum):
    REFUSED = 1
    SEND_PACKS = 2
    HAVE_ALL_PACKS = 3
    COMPLETED = 4


class Dimension(Enum):
    OVERWORLD = 0
    NETHER = 1
    THE_END = 2

    
class GeneratorType(Enum):
    OLD = 0
    INFINITE = 1
    FLAT = 2


class GameMode(Enum):
    SURVIVAL = 0
    CREATIVE = 1
    ADVENTURE = 2


class Difficulty(Enum):
    PEACEFUL = 0
    EASY = 1
    NORMAL = 2
    HARD = 3

    
class GameRuleType(Enum):
    BOOL = 1
    INT = 2
    FLOAT = 3


class PlayerPermission(Enum):
    CUSTOM = 3
    OPERATOR = 2
    MEMBER = 1
    VISITOR = 0


class CommandPermission(Enum):
    NORMAL = 0
    OPERATOR = 1
    HOST = 2
    AUTOMATION = 3
    ADMIN = 4


class AdventureSettingFlag1(Enum):
    WORLD_IMMUTABLE = 0
    NO_PVP = 1
    AUTO_JUMP = 5
    ALLOW_FLIGHT = 6
    NO_CLIP = 7
    WORLD_BUILDER = 8
    FLYING = 9
    MUTED = 10


class AdventureSettingFlag2(Enum):
    BUILD_AND_MINE = 0
    DOORS_AND_SWITCHES = 1
    OPEN_CONTAINERS = 2
    ATTACK_PLAYERS = 3
    ATTACK_MOBS = 4
    OPERATOR = 5
    TELEPORT = 7


class MetaDataType(Enum):
    BYTE = 0
    SHORT = 1
    INT = 2
    FLOAT = 3
    STRING = 4
    SLOT = 5
    INT_VECTOR3 = 6
    LONG = 7
    FLOAT_VECTOR3 = 8


class EntityMetaDataKey(Enum):
    FLAGS = 0
    HEALTH = 1  # minecart/boat
    VARIANT = 2
    COLOR = 3
    NAMETAG = 4
    OWNER_EID = 5
    TARGET_EID = 6
    AIR = 7
    POTION_COLOR = 8  # ARGB!
    POTION_AMBIENT = 9
    # 10 (byte)
    HURT_TIME = 11  # minecart/boat
    HURT_DIRECTION = 12  # minecart/boat
    PADDLE_TIME_LEFT = 13
    PADDLE_TIME_RIGHT = 14
    EXPERIENCE_VALUE = 15  # xp orb
    MINECART_DISPLAY_BLOCK = 16  # id | (data << 16)
    MINECART_DISPLAY_OFFSET = 17
    MINECART_HAS_DISPLAY = 18  # must be 1 for minecart to show block inside
    # 19..22
    ENDERMAN_HELD_ITEM_ID = 23
    ENDERMAN_HELD_ITEM_DAMAGE = 24
    ENTITY_AGE = 25
    # 27 (byte) player-specific flags
    # 28 (int) player "index"?
    BED_POSITION = 29
    FIREBALL_POWER_X = 30
    FIREBALL_POWER_Y = 31
    FIREBALL_POWER_Z = 32
    # 33 (unknown)
    # 34 (float) fishing bobber
    # 35 (float) fishing bobber
    # 36 (float) fishing bobber
    POTION_AUX_VALUE = 37
    LEAD_HOLDER_EID = 38
    SCALE = 39
    INTERACTIVE_TAG = 40  # button text
    NPC_SKIN_ID = 41
    URL_TAG = 42
    MAX_AIR = 43
    MARK_VARIANT = 44
    # 45 (byte) container stuff
    # 46 (int) container stuff
    # 47 (int) container stuff
    BLOCK_TARGET = 48  # ender crystal
    WITHER_INVULNERABLE_TICKS = 49
    WITHER_TARGET_1 = 50
    WITHER_TARGET_2 = 51
    WITHER_TARGET_3 = 52
    # 53 (short)
    BOUNDING_BOX_WIDTH = 54
    BOUNDING_BOX_HEIGHT = 55
    FUSE_LENGTH = 56
    RIDER_SEAT_POSITION = 57
    RIDER_ROTATION_LOCKED = 58
    RIDER_MAX_ROTATION = 59
    RIDER_MIN_ROTATION = 60
    AREA_EFFECT_CLOUD_RADIUS = 61
    AREA_EFFECT_CLOUD_WAITING = 62
    AREA_EFFECT_CLOUD_PARTICLE_ID = 63
    # 64 (int) shulker-related
    SHULKER_ATTACH_FACE = 65
    # 66 (short) shulker-related
    SHULKER_ATTACH_POS = 67
    TRADING_PLAYER_EID = 68
    # 69
    # 70 (byte) command-block
    COMMAND_BLOCK_COMMAND = 71
    COMMAND_BLOCK_LAST_OUTPUT = 72
    COMMAND_BLOCK_TRACK_OUTPUT = 73
    CONTROLLING_RIDER_SEAT_NUMBER = 74
    STRENGTH = 75
    MAX_STRENGTH = 76
    # 77 (int)
    # 78 (int)


class EntityMetaDataFlag(Enum):
    ONFIRE = 0
    SNEAKING = 1
    RIDING = 2
    SPRINTING = 3
    ACTION = 4
    INVISIBLE = 5
    TEMPTED = 6
    INLOVE = 7
    SADDLED = 8
    POWERED = 9
    IGNITED = 10
    BABY = 11
    CONVERTING = 12
    CRITICAL = 13
    CAN_SHOW_NAMETAG = 14
    ALWAYS_SHOW_NAMETAG = 15
    IMMOBILE = 16  # NO_AI
    SILENT = 17
    WALLCLIMBING = 18
    CAN_CLIMB = 19
    SWIMMER = 20
    CAN_FLY = 21
    RESTING = 22
    SITTING = 23
    ANGRY = 24
    INTERESTED = 25
    CHARGED = 26
    TAMED = 27
    LEASHED = 28
    SHEARED = 29
    GLIDING = 30
    ELDER = 31
    MOVING = 32
    BREATHING = 33
    CHESTED = 34
    STACKABLE = 35
    SHOWBASE = 36
    REARING = 37
    VIBRATING = 38
    IDLING = 39
    EVOKER_SPELL = 40
    CHARGE_ATTACK = 41
    WASD_CONTROLLED = 42
    CAN_POWER_JUMP = 43
    LINGER = 44
    HAS_COLLISION = 45
    AFFECTED_BY_GRAVITY = 46
    FIRE_IMMUNE = 47
    DANCING = 48


class PlayerListType(Enum):
    ADD = 0
    REMOVE = 1


class WindowType(Enum):
    INVENTORY = 0
    OFFHAND = 119
    ARMOR = 120
    CREATIVE = 121
    HOTBAR = 122
    FIXED_INVENTORY = 123
    CURSOR = 124

    
class RecipeType(Enum):
    SHAPELESS = 0
    SHAPED = 1
    FURNACE = 2
    FURNACE_DATA = 3
    MULTI = 4
    SHULKER_BOX = 5


class BlockType(Enum):
    """Block IDs

    See https://minecraft.gamepedia.com/Java_Edition_data_values/Block_IDs
    """
    # TODO check ID
    AIR = 0
    STONE = 1
    GRASS = 2
    DIRT = 3
    COBBLESTONE = 4
    PLANKS = 5  # WOODEN_PLANKS
    SAPLING = 6
    BEDROCK = 7
    FLOWING_WATER = 8
    WATER = 9  # STILL_WATER
    FLOWING_LAVA = 10
    LAVA = 11  # STILL_LAVA
    SAND = 12
    GRAVEL = 13
    GOLD_ORE = 14
    IRON_ORE = 15
    COAL_ORE = 16
    LOG = 17  # WOOD
    LEAVES = 18
    SPONGE = 19
    GLASS = 20
    LAPIS_ORE = 21
    LAPIS_BLOCK = 22
    DISPENSER = 23
    SANDSTONE = 24
    NOTEBLOCK = 25  # NOTE_BLOCK
    BED = 26  # BED_BLOCK
    GOLDEN_RAIL = 27  # POWERED_RAIL
    DETECTOR_RAIL = 28
    STICKY_PISTON = 29
    WEB = 30  # COBWEB
    TALLGRASS = 31  # TALL_GRASS
    DEADBUSH = 32  # DEAD_BUSH
    PISTON = 33
    PISTON_HEAD = 34  # PISTONARMCOLLISION, PISTON_ARM_COLLISION
    WOOL = 35
    PISTON_EXTENSION = 36
    YELLOW_FLOWER = 37  # DANDELION
    RED_FLOWER = 38  # POPPY
    BROWN_MUSHROOM = 39
    RED_MUSHROOM = 40
    GOLD_BLOCK = 41
    IRON_BLOCK = 42
    DOUBLE_STONE_SLAB = 43
    STONE_SLAB = 44
    BRICK_BLOCK = 45
    TNT = 46
    BOOKSHELF = 47
    MOSSY_COBBLESTONE = 48  # MOSS_STONE
    OBSIDIAN = 49
    TORCH = 50
    FIRE = 51
    MOB_SPAWNER = 52  # MONSTER_SPAWNER
    OAK_STAIRS = 53   # WOODEN_STAIRS
    CHEST = 54
    REDSTONE_WIRE = 55
    DIAMOND_ORE = 56
    DIAMOND_BLOCK = 57
    CRAFTING_TABLE = 58  # WORKBENCH
    WHEAT = 59  # WHEAT_BLOCK
    FARMLAND = 60
    FURNACE = 61
    LIT_FURNACE = 62  # BURNING_FURNACE
    STANDING_SIGN = 63  # SIGN_POST
    WOODEN_DOOR = 64  # OAK_DOOR_BLOCK
    LADDER = 65
    RAIL = 66
    STONE_STAIRS = 67  # COBBLESTONE_STAIRS
    WALL_SIGN = 68
    LEVER = 69
    STONE_PRESSURE_PLATE = 70
    IRON_DOOR = 71
    WOODEN_PRESSURE_PLATE = 72
    REDSTONE_ORE = 73
    LIT_REDSTONE_ORE = 74  # GLOWING_REDSTONE_ORE
    UNLIT_REDSTONE_TORCH = 75
    REDSTONE_TORCH = 76  # LIT_REDSTONE_TORCH
    STONE_BUTTON = 77
    SNOW_LAYER = 78
    ICE = 79
    SNOW = 80  # SNOW_BLOCK
    CACTUS = 81
    CLAY = 82
    REEDS = 83  # SUGARCANE_BLOCK
    JUKEBOX = 84
    FENCE = 85
    PUMPKIN = 86
    NETHERRACK = 87
    SOUL_SAND = 88
    GLOWSTONE = 89
    PORTAL = 90
    LIT_PUMPKIN = 91  # JACK_O_LANTERN
    CAKE = 92
    UNPOWERED_REPEATER = 93  # REPEATER_BLOCK
    POWERED_REPEATER = 94
    STAINED_GLASS = 95  # INVISIBLEBEDROCK, INVISIBLE_BEDROCK
    TRAPDOOR = 96  # WOODEN_TRAPDOOR
    MONSTER_EGG = 97
    STONEBRICK = 98  # STONE_BRICK, STONE_BRICKS
    BROWN_MUSHROOM_BLOCK = 99
    RED_MUSHROOM_BLOCK = 100
    IRON_BARS = 101
    GLASS_PANE = 102
    MELON_BLOCK = 103
    PUMPKIN_STEM = 104
    MELON_STEM = 105
    VINE = 106  # VINES
    FENCE_GATE = 107  # OAK_FENCE_GATE
    BRICK_STAIRS = 108
    STONE_BRICK_STAIRS = 109
    MYCELIUM = 110
    WATERLILY = 111  # LILY_PAD, WATER_LILY
    NETHER_BRICK = 112
    NETHER_BRICK_FENCE = 113
    NETHER_BRICK_STAIRS = 114
    NETHER_WART = 115
    ENCHANTING_TABLE = 116  # ENCHANTMENT_TABLE
    BREWING_STAND = 117
    CAULDRON = 118
    END_PORTAL = 119
    END_PORTAL_FRAME = 120
    END_STONE = 121
    DRAGON_EGG = 122
    REDSTONE_LAMP = 123
    LIT_REDSTONE_LAMP = 124
    DOUBLE_WOODEN_SLAB = 125  # DROPPER
    WOODEN_SLAB = 126  # ACTIVATOR_RAIL
    COCOA = 127  # COCOA_BLOCK
    SANDSTONE_STAIRS = 128
    EMERALD_ORE = 129
    ENDER_CHEST = 130
    TRIPWIRE_HOOK = 131
    TRIPWIRE = 132  # TRIP_WIRE
    EMERALD_BLOCK = 133
    SPRUCE_STAIRS = 134
    BIRCH_STAIRS = 135
    JUNGLE_STAIRS = 136
    COMMAND_BLOCK = 137
    BEACON = 138
    COBBLESTONE_WALL = 139  # STONE_WALL
    FLOWER_POT = 140
    CARROTS = 141  # CARROT_BLOCK
    POTATOES = 142  # POTATO_BLOCK
    WOODEN_BUTTON = 143
    SKULL = 144  # MOB_HEAD_BLOCK
    ANVIL = 145
    TRAPPED_CHEST = 146
    LIGHT_WEIGHTED_PRESSURE_PLATE = 147
    HEAVY_WEIGHTED_PRESSURE_PLATE = 148
    UNPOWERED_COMPARATOR = 149  # COMPARATOR_BLOCK
    POWERED_COMPARATOR = 150
    DAYLIGHT_DETECTOR = 151  # DAYLIGHT_SENSOR
    REDSTONE_BLOCK = 152
    QUARTZ_ORE = 153  # NETHER_QUARTZ_ORE
    HOPPER = 154
    QUARTZ_BLOCK = 155
    QUARTZ_STAIRS = 156
    ACTIVATOR_RAIL = 157  # DOUBLE_WOODEN_SLAB
    DROPPER = 158  # WOODEN_SLAB
    STAINED_HARDENED_CLAY = 159  # STAINED_CLAY, TERRACOTTA
    STAINED_GLASS_PANE = 160
    LEAVES2 = 161
    LOG2 = 162  # WOOD2
    ACACIA_STAIRS = 163
    DARK_OAK_STAIRS = 164
    SLIME = 165  # SLIME_BLOCK
    BARRIER = 166
    IRON_TRAPDOOR = 167
    PRISMARINE = 168
    SEA_LANTERN = 169  # SEALANTERN
    HAY_BLOCK = 170  # HAY_BALE
    CARPET = 171
    HARDENED_CLAY = 172
    COAL_BLOCK = 173
    PACKED_ICE = 174
    DOUBLE_PLANT = 175
    STANDING_BANNER = 176
    WALL_BANNER = 177
    DAYLIGHT_DETECTOR_INVERTED = 178  # DAYLIGHT_SENSOR_INVERTED
    RED_SANDSTONE = 179
    RED_SANDSTONE_STAIRS = 180
    DOUBLE_STONE_SLAB2 = 181
    STONE_SLAB2 = 182
    SPRUCE_FENCE_GATE = 183
    BIRCH_FENCE_GATE = 184
    JUNGLE_FENCE_GATE = 185
    DARK_OAK_FENCE_GATE = 186
    ACACIA_FENCE_GATE = 187
    SPRUCE_FENCE = 188  # REPEATING_COMMAND_BLOCK
    BRICK_FENCE = 189  # CHAIN_COMMAND_BLOCK
    JUNGLE_FENCE = 190
    DARK_OAK_FENCE = 191
    ACACIA_FENCE = 192
    SPRUCE_DOOR = 193
    BIRCH_DOOR = 194
    JUNGLE_DOOR = 195
    ACACIA_DOOR = 196
    DARK_OAK_DOOR = 197
    END_ROD = 198  # GRASS_PATH
    CHORUS_PLANT = 199  # FRAME_BLOCK, ITEM_FRAME_BLOCK
    CHORUS_FLOWER = 200
    PURPUR_BLOCK = 201
    PURPUR_PILLAR = 202
    PURPUR_STAIRS = 203
    PURPUR_DOUBLE_SLAB = 204
    PURPUR_SLAB = 205  # UNDYED_SHULKER_BOX
    END_BRICKS = 206
    BEETROOTS = 207  # FROSTED_ICE
    GRASS_PATH = 208  # END_ROD
    END_GATEWAY = 209
    REPEATING_COMMAND_BLOCK = 210
    CHAIN_COMMAND_BLOCK = 211
    FROSTED_ICE = 212
    MAGMA = 213
    NETHER_WART_BLOCK = 214
    RED_NETHER_BRICK = 215
    BONE_BLOCK = 216
    STRUCTURE_VOID = 217
    OBSERVER = 218  # SHULKER_BOX
    WHITE_SHULKER_BOX = 219  # PURPLE_GLAZED_TERRACOTTA
    ORANGE_SHULKER_BOX = 220  # WHITE_GLAZED_TERRACOTTA
    MAGENTA_SHULKER_BOX = 221  # ORANGE_GLAZED_TERRACOTTA
    LIGHT_BLUE_SHULKER_BOX = 222  # MAGENTA_GLAZED_TERRACOTTA
    YELLOW_SHULKER_BOX = 223  # LIGHT_BLUE_GLAZED_TERRACOTTA
    LIME_SHULKER_BOX = 224  # YELLOW_GLAZED_TERRACOTTA
    PING_SHULKER_BOX = 225  # LIME_GLAZED_TERRACOTTA
    GRAY_SHULKER_BOX = 226  # PINK_GLAZED_TERRACOTTA
    SILVER_SHULKER_BOX = 227  # GRAY_GLAZED_TERRACOTTA
    CYAN_SHULKER_BOX = 228  # SILVER_GLAZED_TERRACOTTA
    PURPLE_SHULKER_BOX = 229  # CYAN_GLAZED_TERRACOTTA
    BLUE_SHULKER_BOX = 230
    BROWN_SHULKER_BOX = 231  # BLUE_GLAZED_TERRACOTTA
    GREEN_SHULKER_BOX = 232  # BROWN_GLAZED_TERRACOTTA
    RED_SHULKER_BOX = 233  # GREEN_GLAZED_TERRACOTTA
    BLACK_SHULKER_BOX = 234  # RED_GLAZED_TERRACOTTA
    WHITE_GLAZED_TERRACOTTA = 235  # BLACK_GLAZED_TERRACOTTA
    ORANGE_GLAZED_TERRACOTTA = 236  # CONCRETE
    MAGENTA_GLAZED_TERRACOTTA = 237  # CONCRETEPOWDER, CONCRETE_POWDER
    LIGHT_BLUE_GLAZED_TERRACOTTA = 238
    YELLOW_GLAZED_TERRACOTTA = 239
    LIME_GLAZED_TERRACOTTA = 240  # CHORUS_PLANT
    PINK_GLAZED_TERRACOTTA = 241  # STAINED_GLASS
    GRAY_GLAZED_TERRACOTTA = 242
    SILVER_GLAZED_TERRACOTTA = 243  # PODZOL
    CYAN_GLAZED_TERRACOTTA = 244  # BEETROOT_BLOCK
    PURPLE_GLAZED_TERRACOTTA = 245  # STONECUTTER
    BLUE_GLAZED_TERRACOTTA = 246  # GLOWINGOBSIDIAN, GLOWING_OBSIDIAN
    BROWN_GLAZED_TERRACOTTA = 247  # NETHERREACTOR, NETHER_REACTOR
    GREEN_GLAZED_TERRACOTTA = 248  # INFO_UPDATE
    RED_GLAZED_TERRACOTTA = 249  # INFO_UPDATE2
    BLACK_GLAZED_TERRACOTTA = 250  # MOVINGBLOCK, MOVING_BLOCK
    CONCRETE = 251  # OBSERVER
    CONCRETE_POWDER = 252  # STRUCTURE_BLOCK
    UNUSED_FD = 253
    UNUSED_FE = 254
    STRUCTURE_BLOCK = 255


class BiomeType(Enum):
    """Biome IDs

    See https://minecraft.gamepedia.com/Java_Edition_data_values#Biome_IDs
    """
    # TODO check ID
    OCEAN = 0
    PLAINS = 1
    DESERT = 2
    EXTREME_HILLS = 3
    FOREST = 4
    TAIGA = 5
    SWAMPLAND = 6
    RIVER = 7
    HELL = 8
    THE_END = 9
    FROZEN_OCEAN = 10
    FROZEN_RIVER = 11
    ICE_PLAINS = 12
    ICE_MOUNTAINS = 13
    MUSHROOM_ISLAND = 14
    MUSHROOM_ISLAND_SHORE = 15
    BEACH = 16
    DESERT_HILLS = 17
    FOREST_HILLS = 18
    TAIGA_HILLS = 19
    SMALLER_EXTREME_HILLS = 20
    JUNGLE = 21
    JUNGLE_HILLS = 22
    JUNGLE_EDGE = 23
    DEEP_OCEAN = 24
    STONE_BEACH = 25
    COLD_BEACH = 26
    BIRCH_FOREST = 27
    BIRCH_FOREST_HILLS = 28
    ROOFED_FOREST = 29
    TAIGA_COLD = 30
    TAIGA_COLD_HILLS = 31
    REDWOOD_TAIGA = 32
    REDWOOD_TAIGA_HILLS = 33
    EXTREME_HILLS_WITH_TREES = 34
    SAVANNA = 35
    SAVANNA_ROCK = 36
    MESA = 37
    MESA_ROCK = 38
    MESA_CLEAR_ROCK = 39
    THE_VOID = 127
    MUTATED_PLAINS = 129
    MUTATED_DESERT = 130
    MUTATED_EXTREME_HILLS = 131
    MUTATED_FOREST = 132
    MUTATED_TAIGA = 133
    MUTATED_SWAMPLAND = 134
    MUTATED_ICE_FLATS = 140
    MUTATED_JUNGLE = 149
    MUTATED_JUNGLE_EDGE = 151
    MUTATED_BIRCH_FOREST = 155
    MUTATED_BIRCH_FOREST_HILLS = 156
    MUTATED_ROOFED_FOREST = 157
    MUTATED_TAIGA_COLD = 158
    MUTATED_REDWOOD_TAIGA = 160
    MUTATED_REDWOOD_TAIGA_HILLS = 161
    MUTATED_EXTREME_HILLS_WITH_TREES = 162
    MUTATED_SAVANNA = 163
    MUTATED_SAVANNA_ROCK = 164
    MUTATED_MESA = 165
    MUTATED_MESA_ROCK = 166
    MUTATED_MESA_CLEAR_ROCK = 167


class MoveMode(Enum):
    NORMAL = 0
    RESET = 1
    TELEPORT = 2
    PITCH = 3


class SoundType(Enum):
    ITEM_USE_ON = 0
    HIT = 1
    STEP = 2
    FLY = 3
    JUMP = 4
    BREAK = 5
    PLACE = 6
    HEAVY_STEP = 7
    GALLOP = 8
    FALL = 9
    AMBIENT = 10
    AMBIENT_BABY = 11
    AMBIENT_IN_WATER = 12
    BREATHE = 13
    DEATH = 14
    DEATH_IN_WATER = 15
    DEATH_TO_ZOMBIE = 16
    HURT = 17
    HURT_IN_WATER = 18
    MAD = 19
    BOOST = 20
    BOW = 21
    SQUISH_BIG = 22
    SQUISH_SMALL = 23
    FALL_BIG = 24
    FALL_SMALL = 25
    SPLASH = 26
    FIZZ = 27
    FLAP = 28
    SWIM = 29
    DRINK = 30
    EAT = 31
    TAKEOFF = 32
    SHAKE = 33
    PLOP = 34
    LAND = 35
    SADDLE = 36
    ARMOR = 37
    ADD_CHEST = 38
    THROW = 39
    ATTACK = 40
    ATTACK_NO_DAMAGE = 41
    ATTACK_STRONG = 42
    WARN = 43
    SHEAR = 44
    MILK = 45
    THUNDER = 46
    EXPLODE = 47
    FIRE = 48
    IGNITE = 49
    FUSE = 50
    STARE = 51
    SPAWN = 52
    SHOOT = 53
    BREAK_BLOCK = 54
    LAUNCH = 55
    BLAST = 56
    LARGE_BLAST = 57
    TWINKLE = 58
    REMEDY = 59
    UNFECT = 60
    LEVEL_UP = 61
    BOW_HIT = 62
    BULLET_HIT = 63
    EXTINGUISH_FIRE = 64
    ITEM_FIZZ = 65
    CHEST_OPEN = 66
    CHEST_CLOSED = 67
    SHULKERBOX_OPEN = 68
    SHULKERBOX_CLOSED = 69
    POWER_ON = 70
    POWER_OFF = 71
    ATTACH = 72
    DETACH = 73
    DENY = 74
    TRIPOD = 75
    POP = 76
    DROP_SLOT = 77
    NOTE = 78
    THORNS = 79
    PISTON_IN = 80
    PISTON_OUT = 81
    PORTAL = 82
    WATER = 83
    LAVA_POP = 84
    LAVA = 85
    BURP = 86
    BUCKET_FILL_WATER = 87
    BUCKET_FILL_LAVA = 88
    BUCKET_EMPTY_WATER = 89
    BUCKET_EMPTY_LAVA = 90
    RECORD_13 = 91
    RECORD_CAT = 92
    RECORD_BLOCKS = 93
    RECORD_CHIRP = 94
    RECORD_FAR = 95
    RECORD_MALL = 96
    RECORD_MELLOHI = 97
    RECORD_STAL = 98
    RECORD_STRAD = 99
    RECORD_WARD = 100
    RECORD_11 = 101
    RECORD_WAIT = 102
    GUARDIAN_FLOP = 104
    ELDERGUARDIAN_CURSE = 105
    MOB_WARNING = 106
    MOB_WARNING_BABY = 107
    TELEPORT = 108
    SHULKER_OPEN = 109
    SHULKER_CLOSE = 110
    HAGGLE = 111
    HAGGLE_YES = 112
    HAGGLE_NO = 113
    HAGGLE_IDLE = 114
    CHORUSGROW = 115
    CHORUSDEATH = 116
    GLASS = 117
    CAST_SPELL = 118
    PREPARE_ATTACK = 119
    PREPARE_SUMMON = 120
    PREPARE_WOLOLO = 121
    FANG = 122
    CHARGE = 123
    CAMERA_TAKE_PICTURE = 124
    LEASHKNOT_PLACE = 125
    LEASHKNOT_BREAK = 126
    GROWL = 127
    WHINE = 128
    PANT = 129
    PURR = 130
    PURREOW = 131
    DEATH_MIN_VOLUME = 132
    DEATH_MID_VOLUME = 133
    IMITATE_BLAZE = 134
    IMITATE_CAVE_SPIDER = 135
    IMITATE_CREEPER = 136
    IMITATE_ELDER_GUARDIAN = 137
    IMITATE_ENDER_DRAGON = 138
    IMITATE_ENDERMAN = 139
    IMITATE_EVOCATION_ILLAGER = 141
    IMITATE_GHAST = 142
    IMITATE_HUSK = 143
    IMITATE_ILLUSION_ILLAGER = 144
    IMITATE_MAGMA_CUBE = 145
    IMITATE_POLAR_BEAR = 146
    IMITATE_SHULKER = 147
    IMITATE_SILVERFISH = 148
    IMITATE_SKELETON = 149
    IMITATE_SLIME = 150
    IMITATE_SPIDER = 151
    IMITATE_STRAY = 152
    IMITATE_VEX = 153
    IMITATE_VINDICATION_ILLAGER = 154
    IMITATE_WITCH = 155
    IMITATE_WITHER = 156
    IMITATE_WITHER_SKELETON = 157
    IMITATE_WOLF = 158
    IMITATE_ZOMBIE = 159
    IMITATE_ZOMBIE_PIGMAN = 160
    IMITATE_ZOMBIE_VILLAGER = 161
    BLOCK_END_PORTAL_FRAME_FILL = 162
    BLOCK_END_PORTAL_SPAWN = 163
    RANDOM_ANVIL_USE = 164
    BOTTLE_DRAGONBREATH = 165
    DEFAULT = 166
    UNDEFINED = 167


class PlayerActionType(Enum):
    START_BREAK = 0
    ABORT_BREAK = 1
    STOP_BREAK = 2
    GET_UPDATED_BLOCK = 3
    DROP_ITEM = 4
    START_SLEEPING = 5
    STOP_SLEEPING = 6
    RESPAWN = 7
    JUMP = 8
    START_SPRINT = 9
    STOP_SPRINT = 10
    START_SNEAK = 11
    STOP_SNEAK = 12
    DIMENSION_CHANGE_REQUEST = 13  # sent when dying in different dimension
    DIMENSION_CHANGE_ACK = 14  # sent when spawning in a different dimension to tell the server we spawned
    START_GLIDE = 15
    STOP_GLIDE = 16
    BUILD_DENIED = 17
    CONTINUE_BREAK = 18
    SET_ENCHANTMENT_SEED = 20
    UNKNOWN_36 = 36


class TextType(Enum):
    RAW = (0, False, False)
    CHAT = (1, True, False)
    TRANSLATION = (2, False, True)
    POPUP = (3, False, True)
    JUKEBOX_POPUP = (4, False, True)
    TIP = (5, False, False)
    SYSTEM = (6, False, False)
    WHISPER = (7, True, False)
    ANNOUNCEMENT = (8, True, False)

    def __new__(cls, value: int, with_source: bool, with_parameters: bool) -> 'TextType':
        """
        >>> TextType.CHAT
        <TextType.CHAT: 1>
        >>> TextType.CHAT.with_source
        True
        >>> TextType.CHAT.with_parameters
        False
        >>> TextType(1)
        <TextType.CHAT: 1>
        >>> TextType['CHAT']
        <TextType.CHAT: 1>
        """
        obj = object.__new__(cls)
        obj._value_ = value
        obj.with_source = with_source
        obj.with_parameters = with_parameters
        return obj


class EscapeSequence(Enum):
    BLACK = '0'
    DARK_BLUE = '1'
    DARK_GREEN = '2'
    DARK_AQUA = '3'
    DARK_RED = '4'
    DARK_PURPLE = '5'
    GOLD = '6'
    GRAY = '7'
    DARK_GRAY = '8'
    BLUE = '9'
    GREEN = 'a'
    AQUA = 'b'
    RED = 'c'
    LIGHT_PURPLE = 'd'
    YELLOW = 'e'
    WHITE = 'f'
    OBFUSCATED = 'k'
    BOLD = 'l'
    STRIKE_THROUGH = 'm'
    UNDERLINE = 'n'
    ITALIC = 'o'
    RESET = 'r'

    def __new__(cls, value: str) -> 'EscapeSequence':
        """
        >>> EscapeSequence.BLACK
        <EscapeSequence.BLACK: '§0'>
        >>> EscapeSequence('§0')
        <EscapeSequence.BLACK: '§0'>
        >>> EscapeSequence['BLACK']
        <EscapeSequence.BLACK: '§0'>
        """
        obj = object.__new__(cls)
        obj._value_ = b'\xc2\xa7'.decode() + value  # '§[value]'
        return obj


class EntityEventType(Enum):
    HURT_ANIMATION = 2
    DEATH_ANIMATION = 3
    ARM_SWING = 4
    # 5
    TAME_FAIL = 6
    TAME_SUCCESS = 7
    SHAKE_WET = 8
    USE_ITEM = 9
    EAT_GRASS_ANIMATION = 10
    FISH_HOOK_BUBBLE = 11
    FISH_HOOK_POSITION = 12
    FISH_HOOK_HOOK = 13
    FISH_HOOK_TEASE = 14
    SQUID_INK_CLOUD = 15
    ZOMBIE_VILLAGER_CURE = 16
    # 17
    RESPAWN = 18
    IRON_GOLEM_OFFER_FLOWER = 19
    IRON_GOLEM_WITHDRAW_FLOWER = 20
    LOVE_PARTICLES = 21  # breeding
    # 22-23
    WITCH_SPELL_PARTICLES = 24
    FIREWORK_PARTICLES = 25
    # 26
    SILVERFISH_SPAWN_ANIMATION = 27
    # 28
    WITCH_DRINK_POTION = 29
    WITCH_THROW_POTION = 30
    MINECART_TNT_PRIME_FUSE = 31
    # 32-33
    PLAYER_ADD_XP_LEVELS = 34
    ELDER_GUARDIAN_CURSE = 35
    AGENT_ARM_SWING = 36
    ENDER_DRAGON_DEATH = 37
    DUST_PARTICLES = 38  # not sure what this is
    # 39-56
    EATING_ITEM = 57
    # 58-59
    BABY_ANIMAL_FEED = 60  # green particles, like bonemeal on crops
    DEATH_SMOKE_CLOUD = 61
    COMPLETE_TRADE = 62
    REMOVE_LEASH = 63  # data 1 = cut leash
    # 64
    CONSUME_TOTEM = 65
    PLAYER_CHECK_TREASURE_HUNTER_ACHIEVEMENT = 66
    ENTITY_SPAWN = 67  # used for MinecraftEventing stuff, not needed
    DRAGON_PUKE = 68  # they call this puke particles
    ITEM_ENTITY_MERGE = 69


class InventoryTransactionType(Enum):
    NORMAL = 0
    MISMATCH = 1
    USE_ITEM = 2
    USE_ITEM_ON_ENTITY = 3
    RELEASE_ITEM = 4


class SourceType(Enum):
    CONTAINER = 0
    WORLD = 2
    CREATIVE = 3
    TODO = 99999


class EntityType(Enum):
    CHICKEN = 10
    COW = 11
    PIG = 12
    SHEEP = 13
    WOLF = 14
    VILLAGER = 15
    MOOSHROOM = 16
    SQUID = 17
    RABBIT = 18
    BAT = 19
    IRON_GOLEM = 20
    SNOW_GOLEM = 21
    OCELOT = 22
    HORSE = 23
    DONKEY = 24
    MULE = 25
    SKELETON_HORSE = 26
    ZOMBIE_HORSE = 27
    POLAR_BEAR = 28
    LLAMA = 29
    PARROT = 30
    # 31 NONE
    ZOMBIE = 32
    CREEPER = 33
    SKELETON = 34
    SPIDER = 35
    ZOMBIE_PIGMAN = 36
    SLIME = 37
    ENDERMAN = 38
    SILVERFISH = 39
    CAVE_SPIDER = 40
    GHAST = 41
    MAGMA_CUBE = 42
    BLAZE = 43
    ZOMBIE_VILLAGER = 44
    WITCH = 45
    STRAY = 46
    HUSK = 47
    WITHER_SKELETON = 48
    GUARDIAN = 49
    ELDER_GUARDIAN = 50
    NPC = 51
    WITHER = 52
    ENDER_DRAGON = 53
    SHULKER = 54
    ENDERMITE = 55
    LEARN_TO_CODE_MASCOT = 56
    VINDICATOR = 57
    # 58-60 NONE
    ARMOR_STAND = 61
    TRIPOD_CAMERA = 62
    PLAYER = 63
    ITEM = 64
    TNT = 65
    FALLING_BLOCK = 66
    MOVING_BLOCK = 67
    XP_BOTTLE = 68
    XP_ORB = 69
    EYE_OF_ENDER_SIGNAL = 70
    ENDER_CRYSTAL = 71
    FIREWORKS_ROCKET = 72
    # 73-75 NONE
    SHULKER_BULLET = 76
    FISHING_HOOK = 77
    CHALKBOARD = 78
    DRAGON_FIREBALL = 79
    ARROW = 80
    SNOWBALL = 81
    EGG = 82
    PAINTING = 83
    MINECART = 84
    LARGE_FIREBALL = 85
    SPLASH_POTION = 86
    ENDER_PEARL = 87
    LEASH_KNOT = 88
    WITHER_SKULL = 89
    BOAT = 90
    WITHER_SKULL_DANGEROUS = 91
    LIGHTNING_BOLT = 93
    SMALL_FIREBALL = 94
    AREA_EFFECT_CLOUD = 95
    HOPPER_MINECART = 96
    TNT_MINECART = 97
    CHEST_MINECART = 98
    # 99 NONE
    COMMAND_BLOCK_MINECART = 100
    LINGERING_POTION = 101
    LLAMA_SPIT = 102
    EVOCATION_FANG = 103
    EVOCATION_ILLAGER = 104
    VEX = 105


if __name__ == '__main__':
    import doctest
    doctest_result = doctest.testmod()
