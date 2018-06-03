import textwrap

import tdl

import colors
import constants


def menu(con, root, header, options, width):
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
    root.blit(window, x, y, width, height, 0, 0)


def inventory_menu(con, root, header, inventory, inventory_width):
    # Show a menu with each item of the inventory as an option
    if len(inventory.items) == 0:
        options = ['Inventory is empty']
    else:
        options = [item.name for item in inventory.items]

    menu(con, root, header, options, inventory_width)