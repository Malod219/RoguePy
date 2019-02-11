import libtcodpy as libtcod

from random_utils import from_dungeon_level
from render_functions import RenderOrder
from components.ai import BasicMonster
from components.fighter import Fighter
from entity import Entity
from components.item import Item
from components.equippable import Equippable
from components.equipment import EquipmentSlots
from item_functions import heal, cast_lightning, cast_fireball
from game_messages import Message

def get_content(self):

    monster_chances = {'bat': from_dungeon_level([[100, 0], [20, 2], [5, 4]],self.dungeon_level),
                       'orc': from_dungeon_level([[80, 0], [0, 7]],self.dungeon_level),
                       'troll': from_dungeon_level([[15, 3], [60, 5], [80, 7]], self.dungeon_level),
                       'goblin': from_dungeon_level([[30, 0], [50, 3], [40,6]],self.dungeon_level),
                       }

    item_chances = {'healing_potion': 35,
                    'sword': from_dungeon_level([[5, 4]], self.dungeon_level),
                    'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
                    'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
                    'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
                    }
    return monster_chances, item_chances


def create_entity(x , y, monster_choice):
    if monster_choice == 'orc':
        fighter_component = Fighter(hp=20, defense=0, power=4, xp=35)
        ai_component = BasicMonster()
        monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True, render_order=RenderOrder.ACTOR,
                         fighter=fighter_component, ai=ai_component)
    elif monster_choice == 'troll':
        fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
        ai_component = BasicMonster()
        monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR,
                         fighter=fighter_component,
                         ai=ai_component)
    elif monster_choice == 'bat':
        fighter_component = Fighter(hp=10, defense=1, power=2, xp=10)
        ai_component = BasicMonster()
        monster = Entity(x, y, 'b', libtcod.darker_gray, 'Bat', blocks=True, render_order=RenderOrder.ACTOR,
                         fighter=fighter_component,
                         ai=ai_component)
    elif monster_choice == 'goblin':
        fighter_component = Fighter(hp=30, defense=2, power=3, xp=50)
        ai_component = BasicMonster()
        monster = Entity(x, y, 'g', libtcod.green, 'Goblin', blocks=True, render_order=RenderOrder.ACTOR,
                         fighter=fighter_component,
                         ai=ai_component)

    else:
        fighter_component = Fighter(hp=1, defense=1, power=1, xp=1)
        ai_component = BasicMonster()
        monster = Entity(x, y, '^', libtcod.darker_magenta, 'Figment', blocks=True, render_order=RenderOrder.ACTOR,
                         fighter=fighter_component,
                         ai=ai_component)
    return monster


def create_item(x, y, item_choice):

    if item_choice == 'healing_potion':
        item_component = Item(use_function=heal, amount=40)
        item = Entity(x, y, '!', libtcod.violet, 'Healing Salve', render_order=RenderOrder.ITEM,
                      item=item_component)

    elif item_choice == 'sword':
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
        item = Entity(x, y, '/', libtcod.sky, 'Sword', equippable=equippable_component)

    elif item_choice == 'shield':
        equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
        item = Entity(x, y, '[', libtcod.darker_amber, 'Shield', equippable=equippable_component)

    elif item_choice == 'fireball_scroll':
        item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
            'Left-click a target tile for the fireball, or right click to cancel.', libtcod.light_cyan),
                              damage=25, radius=3)
        item = Entity(x, y, '#', libtcod.yellow, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                      item=item_component)

    else:
        item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
        item = Entity(x, y, '!', libtcod.yellow, 'Scroll of Lightning', render_order=RenderOrder.ITEM,
                      item=item_component)

    return item


