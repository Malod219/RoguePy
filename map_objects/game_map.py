import libtcodpy as libtcod
from random import randint

from entity import Entity
from game_messages import Message
from map_objects.tile import Tile
from map_objects.rectangle import Rect
from map_objects.cellularAutomataGen import make_cave_room
from components.stairs import Stairs
from render_functions import RenderOrder
from random_utils import from_dungeon_level, random_choice_from_dict
from map_objects.content import get_content, create_entity, create_item


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level
        self.theme = randint(0,1)

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def clean_up_boundary(self, map_width, map_height):
        for x, row in enumerate(self.tiles):
            for y, col in enumerate(row):
                if x in (0, 1, map_width-1, map_width-2) or y in (0, 1, map_height-1, map_height-2):
                    self.tiles[x][y].name = None
                    self.tiles[x][y].blocked = True
                    self.tiles[x][y].block_sight = True

    def make_map(self , max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            #random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            #random position without going out of bounds
            x = randint(1, map_width - w - 2)
            y = randint(1, map_height - h - 2)

            #Make room
            new_room = Rect(x, y, w, h)

            #run through other rooms to check intersections
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                #No intersections so valid
                self.create_room(new_room, map_width, map_height)
                #center coordinates of new room
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    #All rooms after first
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    #flip a coin for tunnels
                    if randint(0, 1) == 1:
                        #first move horizontal then vertical
                        self.create_h_tunnel(prev_x, new_x, prev_y, randint(1,4))
                        self.create_v_tunnel(prev_y, new_y, new_x, randint(1,4))
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x, randint(1,4))
                        self.create_h_tunnel(prev_x, new_x, new_y, randint(1,4))
                #finally append room to list and increment room count
                self.place_entities(new_room, entities)
                rooms.append(new_room)
                num_rooms += 1
        self.clean_up_boundary(map_width, map_height)

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def create_room(self, room, map_width, map_height):
        room_choice = randint(0, 1)

        if room_choice == 0:
            for x in range(room.x1+1, room.x2):
                for y in range(room.y1+1, room.y2):
                    self.tiles[x][y].blocked = False
                    self.tiles[x][y].block_sight = False
        elif room_choice == 1:
            room_width = room.x2 - room.x1
            room_height = room.y2 - room.y1
            make_cave_room(self, room_width, room_height, room.x1, room.y1, map_width, map_height)

    def create_h_tunnel(self, x1, x2, y, tunnel_width):
        for tunnel in range(tunnel_width):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.tiles[x][y+tunnel].blocked = False
                self.tiles[x][y+tunnel].block_sight = False

    def create_v_tunnel(self, y1, y2, x, tunnel_width):
        for tunnel in range(tunnel_width):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.tiles[x+tunnel][y].blocked = False
                self.tiles[x+tunnel][y].block_sight = False

    def place_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level([[2, 1], [3,4], [5,6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1,1], [2,4]], self.dungeon_level)

        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances, item_chances = get_content(self)

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            #choose a random location in room
            if self.tiles[x][y].blocked == True:
                skip = True
            else:
                skip = False

            if not any([entity for entity in entities if entity.x == x and entity.y == y ]) and not skip:
                monster_choice = random_choice_from_dict(monster_chances)
                monster = create_entity(x, y, monster_choice)
                entities.append(monster)
        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            #choose a random location in room
            if self.tiles[x][y].blocked == True:
                skip = True
            else:
                skip = False

            if not any([entity for entity in entities if entity.x == x and entity.y == y ]) and not skip:
                item_choice = random_choice_from_dict(item_chances)

                item = create_item(x, y, item_choice)

                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        self.theme = randint(0, 1)
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

        player.fighter.heal(int(player.fighter.max_hp / 2))

        message_log.add_message(Message('You take a moment to rest and recover your strength', libtcod.light_violet))
        return entities
