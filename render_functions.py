import colors
import constants


def render_all(con, entities, game_map, fov_recompute, root_console):
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

            elif game_map.explored[x][y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.dark_wall)
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.dark_ground)

    # Draw all entities in the list
    for entity in entities:
        draw_entity(con, entity, game_map.fov)

    root_console.blit(con, 0, 0, constants.screen_width, constants.screen_height, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov):
    if fov[entity.x, entity.y]:
        con.draw_char(entity.x, entity.y, entity.char, entity.color, bg=None)


def clear_entity(con, entity):
    # Erase the character that represents this object
    con.draw_char(entity.x, entity.y, ' ', entity.color, bg=None)