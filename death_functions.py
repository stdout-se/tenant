from game_messages import Message
from game_states import GameStates
import colors
from render_functions import RenderOrder


def kill_player(player):
    player.char = '%'
    player.color = colors.dark_red

    return Message('You died!', colors.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = Message(f'{monster.name.capitalize()} is dead!', colors.orange)

    monster.char = '%'
    monster.color = colors.dark_red
    monster.blocks = False
    monster.fither = None
    monster.ai = None
    monster.name = f'remains of {monster.name}'
    monster.render_order = RenderOrder.CORPSE

    return death_message
