import colors
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from map_utils import GameMap, make_map
from render_functions import RenderOrder


def get_game_variables():
    fighter_component = Fighter(hp=100, defense=1, power=4)
    inventory_component = Inventory(26)
    level_component = Level()
    player = Entity(0, 0, '@', colors.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component)
    entities = [player]

    game_map = GameMap()
    make_map(game_map, player, entities)

    message_log = MessageLog()

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
