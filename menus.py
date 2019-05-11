import tcod as libtcod
from typing import List

import colors
import constants


def menu(con, header: str, options: List[str], width: int):
    if len(options) > 26:
        raise ValueError('Cannot have more than 26 options')

    # Calculate total height for the header (after textwrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, constants.screen_height, header)
    height = len(options) + header_height

    # Create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # Print the header, with wrapped text
    libtcod.console_set_default_foreground(window, colors.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = f'({chr(letter_index)}) {option_text}'
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # Blit the contents of "window" to the root console
    x = constants.screen_width // 2 - width // 2
    y = constants.screen_height // 2 - height // 2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(con, header: str, player, inventory_width: int):
    # Show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append(f'{item.name} (in main hand)')
            elif player.equipment.off_hand == item:
                options.append(f'{item.name} (in off hand)')
            else:
                options.append(item.name)

    menu(con, header, options, inventory_width)


def main_menu(con, background_image):
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    title = 'TENANT SIMULATOR'
    libtcod.console_set_default_foreground(0, colors.light_yellow)
    libtcod.console_print_ex(0, constants.screen_width // 2, constants.screen_height // 2 - 4, libtcod.BKGND_NONE,
                             libtcod.CENTER, title)

    title = 'By name'
    libtcod.console_print_ex(0, constants.screen_width // 2, constants.screen_height - 2, libtcod.BKGND_NONE,
                             libtcod.CENTER, title)

    menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24)


def level_up_menu(con, header: str, player, menu_width: int):
    options = [f'Constitution (+20 HP, from {player.fighter.max_hp})',
               f'Strength (+1 attack, from {player.fighter.power})',
               f'Agility (+1 defense, from {player.fighter.defense})']

    menu(con, header, options, menu_width)


def character_screen(player, character_screen_width: int, character_screen_height: int):
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, colors.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character Information')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Level: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience: {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT,
                                  'Experience to Level: {0}'.format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Attack: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defense: {0}'.format(player.fighter.defense))

    x = constants.screen_width // 2 - character_screen_width // 2
    y = constants.screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)


def message_box(con, header: str, width: int):
    menu(con, header, [], width)
