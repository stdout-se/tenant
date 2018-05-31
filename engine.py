import tdl

import colors
import constants
from entity import Entity, get_blocking_entities_at_location
from input_handlers import handle_keys
from map_utils import make_map, GameMap
from render_functions import render_all, clear_all


def main():
    player = Entity(0, 0, '@', colors.white, 'Player', blocks=True)
    entities = [player]

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(constants.screen_width, constants.screen_height, title='Lanlord')
    con = tdl.Console(constants.screen_width, constants.screen_height)

    game_map = GameMap()
    make_map(game_map, player, entities)

    fov_recompute = True

    while not tdl.event.is_window_closed():
        if fov_recompute:
            game_map.compute_fov(player.x, player.y,
                                 fov=constants.fov_algorithm,
                                 radius=constants.fov_radius,
                                 light_walls=constants.fov_light_walls)

        render_all(con, entities, game_map, fov_recompute, root_console)
        tdl.flush()

        clear_all(con, entities)

        fov_recompute = False

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None

        if not user_input:
            continue

        action = handle_keys(user_input)

        move = action.get('move')
        exit_ = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if game_map.walkable[destination_x, destination_y]:
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    print('You attack the ' + target.name)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

        if exit_:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())


if __name__ == '__main__':
    main()
