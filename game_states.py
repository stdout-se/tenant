from enum import Enum, auto


class GameStates(Enum):
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
    PLAYERS_TURN = auto()
    SHOW_INVENTORY = auto()
    DROP_INVENTORY = auto()
    TARGETING = auto()
