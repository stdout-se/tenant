from enum import Enum, auto


class GameStates(Enum):
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
    PLAYERS_TURN = auto()
