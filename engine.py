# http://rogueliketutorials.com/tdl/6
# Continue: Create a new python file called death_functions.py

import tdl

import colors
import constants
from components.fighter import Fighter
from entity import Entity, get_blocking_entities_at_location
from game_states import GameStates
from input_handlers import handle_keys
from map_utils import make_map, GameMap
from render_functions import render_all, clear_all


def main():
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', colors.white, 'Player', blocks=True, fighter=fighter_component)
    entities = [player]

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(constants.screen_width, constants.screen_height, title='Lanlord')
    con = tdl.Console(constants.screen_width, constants.screen_height)

    game_map = GameMap()
    make_map(game_map, player, entities)

    fov_recompute = True

    game_state = GameStates.PLAYERS_TURN

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

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if game_map.walkable[destination_x, destination_y]:
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit_:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                print(message)

            if dead_entity:
                pass  # We'll do something here momentarily

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            print(message)

                        if dead_entity:
                            pass
                else:
                    game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
