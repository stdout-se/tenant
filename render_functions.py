import tcod as libtcod
from enum import Enum
from typing import Tuple

import colors
import constants
from game_states import GameStates
from menus import inventory_menu, level_up_menu, character_screen


class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4


def get_names_under_mouse(mouse_coordinates: Tuple[int, int], entities, game_map):
    x, y = mouse_coordinates

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and game_map.fov[entity.x, entity.y]]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x: int, y: int, total_width: int, name: str, value: int, maximum: int,
               bar_color: Tuple[int, int, int], back_color: Tuple[int, int, int], string_color: Tuple[int, int, int]):
    # Render a bar (HP, experience, etc). First calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # Render the background first
    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    # Now render the bar on top
    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    # Finally, some centered text with the values
    text = f'{name}: {value}/{maximum}'
    libtcod.console_set_default_foreground(panel, string_color)
    libtcod.console_print_ex(panel, x + total_width // 2, y, libtcod.BKGND_NONE, libtcod.CENTER, text)


def render_all(con, panel, entities, player, game_map, fov_recompute: bool, message_log,
               mouse_coordinates: Tuple[int, int], game_state):
    # Draw all the tiles in the game map
    if fov_recompute:
        for x, y, in game_map:
            wall = not game_map.transparent[x, y]

            if game_map.fov[x, y]:
                if wall:
                    libtcod.console_set_char_background(con, x, y, colors.light_wall, libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, x, y, colors.light_ground, libtcod.BKGND_SET)

                game_map.explored[x][y] = True

            elif game_map.explored[x][y] or constants.debug:
                if wall:
                    libtcod.console_set_char_background(con, x, y, colors.dark_wall, libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, x, y, colors.dark_ground, libtcod.BKGND_SET)

    entities_in_render_order = sorted(entities, key=lambda e: e.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, game_map)

    # noinspection PyTypeChecker
    libtcod.console_blit(con, 0, 0, constants.screen_width, constants.screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, colors.black)
    libtcod.console_clear(panel)

    # Print the game messages, one line at a time
    for y, message in enumerate(message_log.messages):
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, constants.message_x, y + 1, libtcod.BKGND_NONE, libtcod.LEFT, message.text)

    # Show player health bar
    render_bar(panel, 1, 1, constants.bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, colors.light_red,
               colors.darker_red, colors.white)

    # Show dungeon level
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT, f'Dungeon Level: {game_map.dungeon_level}')

    # Show entities under the mouse cursor
    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse_coordinates, entities, game_map))

    # noinspection PyTypeChecker
    libtcod.console_blit(panel, 0, 0, constants.screen_width, constants.panel_height, 0, 0, constants.panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel\n'

        inventory_menu(con, inventory_title, player, 50)

    if game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up! Choose a state to raise:', player, 40)

    if game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, game_map):
    if game_map.fov[entity.x, entity.y] or (entity.stairs and game_map.explored[entity.x][entity.y]) or constants.debug:
        # If in player's FOV, it's a previously explored stairs or debug mode
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # Erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
