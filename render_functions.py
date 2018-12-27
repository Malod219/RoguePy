import libtcodpy as libtcod

from enum import Enum

from game_states import GameStates

from menus import inventory_menu, level_up_menu, character_screen

class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4

def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value)/maximum * total_width)

    libtcod.console_set_default_background(panel, bar_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, back_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width/2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))
    

def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width,
               panel_height, panel_y, mouse, colors, game_state):
    fov_recompute = True

    center_x = int(screen_width/2)
    center_y = int(screen_height/2)

    camera_x = player.x
    camera_y = player.y

    top_left_x = camera_x - center_x
    top_left_y = camera_y - center_y

    #Draw tiles
    if fov_recompute:
        libtcod.console_clear(con)
        for y in range(screen_height-panel_height):
            tile_y = y + top_left_y
            for x in range(screen_width):

                tile_x = x + top_left_x
                if tile_x >= game_map.width-1:
                    tile_x = game_map.width-1
                if tile_y >= game_map.height:
                    tile_y = game_map.height-1
                if tile_x < 0:
                    tile_x = 0
                if tile_y < 0:
                    tile_y = 0
                tile = game_map.tiles[tile_x][tile_y]

                visible = libtcod.map_is_in_fov(fov_map, tile_x, tile_y)
                wall = tile.block_sight

                if visible:
                    if wall:
                        libtcod.console_put_char_ex(con, x, y, colors.get('light_wall')[0], colors.get('light_wall')[1],
                                                    colors.get('light_wall')[2])
                    else:
                        libtcod.console_put_char_ex(con, x, y, colors.get('light_ground')[0], colors.get('light_ground')[1],
                                                    colors.get('light_ground')[2])
                        
                    tile.explored = True
                elif tile.explored:
                    if wall:
                        libtcod.console_put_char_ex(con, x, y, colors.get('dark_wall')[0], colors.get('dark_wall')[1],
                                                    colors.get('dark_wall')[2])
                    else:
                        libtcod.console_put_char_ex(con, x, y, colors.get('dark_ground')[0], colors.get('dark_ground')[1],
                                                    colors.get('dark_ground')[2])

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    # Draw entities
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map,top_left_x,top_left_y)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_clear(panel)

    y = 0
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    libtcod.console_set_default_foreground(panel, libtcod.light_orange)
    libtcod.console_print_frame(panel, 0, 0, screen_width, panel_height, False, libtcod.BKGND_NONE,"Message Log")

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_grey)
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Dungeon level: {0}'.format(game_map.dungeon_level))

    libtcod.console_set_default_foreground(panel, libtcod.light_grey)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))
    
    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)

    if game_state == GameStates.LEVELED_UP:
        level_up_title = 'Press the key next to an option to level up accordingly.\n'

        level_up_menu(con, level_up_title, player, 50, screen_width, screen_height)

    if game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map, top_left_x, top_left_y):
    # Put entity's character and foreground colour in spot
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x-top_left_x, entity.y-top_left_y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # Put blank character in spot
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
