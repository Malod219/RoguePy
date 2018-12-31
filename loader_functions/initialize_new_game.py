import libtcodpy as libtcod

from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.equippable import Equippable
from components.level import Level

from entity import Entity

from equipment_slots import EquipmentSlots

from game_messages import MessageLog

from game_states import GameStates

from map_objects.game_map import GameMap

from render_functions import RenderOrder


def get_constants():
    window_title = 'Roguelike'

    screen_width = 160
    screen_height = 90

    bar_width = 40
    panel_height = 10
    panel_y = screen_height - panel_height

    message_x = 44
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 50
    map_height = 50

    room_max_size = 10
    room_min_size = 6
    max_rooms = 40

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 4
    max_items_per_room = 4

    chrome = [libtcod.Color(100, 100, 100), libtcod.Color(16, 36, 44),
              libtcod.Color(13, 28, 34),  libtcod.Color(0, 10, 14)]
    earth = [libtcod.Color(100, 67, 51), libtcod.Color(71, 45, 32),
             libtcod.Color(44, 14, 0),   libtcod.Color(47, 19, 10)]


    # This is for tiles.
    # ID : ['Character', Foreground Colour, Background Colour]
    colors = {
        # Walls
            # Visible
            'w_earth_light': ['#', earth[0], earth[1]],
            # Out of view
            'w_earth_dark': ['#', earth[2], earth[3]],
        # Floor tiles
            # Visible
            'f_earth_light': [',', earth[0], earth[1]],
            # Out of view
            'f_earth_dark': [',', earth[2], earth[3]],

        '0_dark_wall': ['#', libtcod.Color(0, 0, 100), libtcod.Color(0, 0, 0)],
        '0_dark_ground': ['.', libtcod.Color(50, 50, 100), libtcod.Color(0, 0, 0)],
        '0_light_wall': ['#', libtcod.Color(130, 110, 50), libtcod.Color(0, 0, 0)],
        '0_light_ground': ['.', libtcod.Color(200, 180, 50), libtcod.Color(0, 0, 0)],

        '1_light_wall': ['#', chrome[0], chrome[1]],
        '1_light_ground': ['.', chrome[0], chrome[1]],
        '1_dark_wall': ['#', chrome[2], chrome[3]],
        '1_dark_ground': ['.', chrome[2], chrome[3]],

        '2_light_wall': ['#', earth[0], earth[1]],
        '2_dark_wall': ['#', earth[2], earth[3]],
        '2_light_ground': [',', earth[0], earth[1]],
        '2_dark_ground': ['.', earth[2], earth[3]],
        }

    constants = {
        'window_title':window_title,
        'screen_width':screen_width,
        'screen_height':screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'colors': colors,
    }

    return constants


def get_game_variables(constants):
    fighter_component = Fighter(hp=100, defense=1, power=2)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component,
                    equipment=equipment_component)
    entities = [player]

    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2, max_hp_bonus=20)
    dagger = Entity(0,0, '-', libtcod.sky, 'Dagger', equippable=equippable_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
