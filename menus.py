import textwrap

import tdl

import colors
import constants


def menu(con, root_console, header, options, width):
    if len(options) > 26:
        raise ValueError('Cannot have more than 26 options')

    # Calculate total height for the header (after textwrap) and one line per option
    header_wrapped = textwrap.wrap(header, width)
    header_height = len(header_wrapped)
    height = len(options) + header_height

    # Create an off-screen console that represents the menu's window
    window = tdl.Console(width, height)

    # Print the header, with wrapped text
    window.draw_rect(0, 0, width, height, None, fg=colors.white, bg=None)
    for i, line in enumerate(header_wrapped):
        window.draw_str(0, 0 + i, header_wrapped[i])

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = f'({chr(letter_index)}) {option_text}'
        window.draw_str(0, y, text, bg=None)
        y += 1
        letter_index += 1

    # Blit the contents of "window" to the root console
    x = constants.screen_width // 2 - width // 2
    y = constants.screen_height // 2 - height // 2
    root_console.blit(window, x, y, width, height, 0, 0)


def inventory_menu(con, root_console, header, player, inventory_width):
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

    menu(con, root_console, header, options, inventory_width)


def main_menu(con, root_console, background_image):
    background_image.blit_2x(root_console, 0, 0)

    title = 'TENANT SIMULATOR'
    center = (constants.screen_width - len(title)) // 2
    root_console.draw_str(center, constants.screen_height // 2 - 4, title, bg=None, fg=colors.light_yellow)

    title = 'By name'
    center = (constants.screen_width - len(title)) // 2
    root_console.draw_str(center, constants.screen_height - 2, title, bg=None, fg=colors.light_yellow)

    menu(con, root_console, '', ['Play a new game', 'Continue last game', 'Quit'], 24)


def level_up_menu(con, root_console, header, player, menu_width):
    options = [f'Constitution (+20 HP, from {player.fighter.max_hp})',
               f'Strength (+1 attack, from {player.fighter.power})',
               f'Agility (+1 defense, from {player.fighter.defense})']

    menu(con, root_console, header, options, menu_width)


def character_screen(root_console, player, character_screen_width, character_screen_height):
    window = tdl.Console(character_screen_width, character_screen_height)

    window.draw_rect(0, 0, character_screen_width, character_screen_height, None, fg=colors.white, bg=None)

    window.draw_str(0, 1, 'Character Information')
    window.draw_str(0, 2, 'Level: {0}'.format(player.level.current_level))
    window.draw_str(0, 3, 'Experience: {0}'.format(player.level.current_xp))
    window.draw_str(0, 4, 'Experience to Level: {0}'.format(player.level.experience_to_next_level))
    window.draw_str(0, 6, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    window.draw_str(0, 7, 'Attack: {0}'.format(player.fighter.power))
    window.draw_str(0, 8, 'Defense: {0}'.format(player.fighter.defense))

    x = constants.screen_width // 2 - character_screen_width // 2
    y = constants.screen_height // 2 - character_screen_height // 2
    root_console.blit(window, x, y, character_screen_width, character_screen_height, 0, 0)


def message_box(con, root_console, header, width):
    menu(con, root_console, header, [], width)
