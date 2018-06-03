from enum import Enum

import colors
import constants
from game_states import GameStates
from menus import inventory_menu


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


def get_names_under_mouse(mouse_coordinates, entities, game_map):
    x, y = mouse_coordinates

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and game_map.fov[entity.x, entity.y]]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, string_color):
    # Render a bar (HP, experience, etc). First calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # Render the background first
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)

    # Now render the bar on top
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)

    # Finally, some centered text with the values
    text = f'{name}: {value}/{maximum}'
    x_centered = x + (total_width - len(text)) // 2

    panel.draw_str(x_centered, y, text, fg=string_color, bg=None)


def render_all(con, panel, entities, player, game_map, fov_recompute, root_console, message_log, mouse_coordinates,
               game_state):
    # Draw all the tiles in the game map
    if fov_recompute:
        for x, y, in game_map:
            wall = not game_map.transparent[x, y]

            if game_map.fov[x, y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.light_wall)
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.light_ground)

                game_map.explored[x][y] = True

            elif game_map.explored[x][y] or constants.debug:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.dark_wall)
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.dark_ground)

    entities_in_render_order = sorted(entities, key=lambda e: e.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, game_map.fov)

    root_console.blit(con, 0, 0, constants.screen_width, constants.screen_height, 0, 0)

    panel.clear(fg=colors.white, bg=colors.black)

    # Print the game messages, one line at a time
    for y, message in enumerate(message_log.messages):
        panel.draw_str(constants.message_x, y + 1, message.text, bg=None, fg=message.color)

    # Show player health bar
    render_bar(panel, 1, 1, constants.bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, colors.light_red,
               colors.darker_red, colors.white)

    # Show entities under the mouse cursor
    panel.draw_str(1, 0, get_names_under_mouse(mouse_coordinates, entities, game_map))

    root_console.blit(panel, 0, constants.panel_y, constants.screen_width, constants.panel_height, 0, 0)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel\n'

        inventory_menu(con, root_console, inventory_title, player.inventory, 50)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov):
    if fov[entity.x, entity.y] or constants.debug:
        con.draw_char(entity.x, entity.y, entity.char, entity.color, bg=None)


def clear_entity(con, entity):
    # Erase the character that represents this object
    con.draw_char(entity.x, entity.y, ' ', entity.color, bg=None)
