import libtcodpy as libtcod
import xp_loader
import gzip


def foregroundLayer(screen_width, screen_height):
    xp_file = gzip.open('Title.xp')
    raw_data = xp_file.read()
    xp_file.close()

    xp_data = xp_loader.load_xp_string(raw_data)

    console_width = xp_data['width']
    console_height = xp_data['height']

    layer_0_console = libtcod.console_new(xp_data['layer_data'][0]['width'], xp_data['layer_data'][0]['height'])

    xp_loader.load_layer_to_console(layer_0_console, xp_data['layer_data'][0])

    libtcod.console_blit(layer_0_console, -10, 16, console_width, console_height, 0, 0, 0)


def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, screen_width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_print_frame(0, x - 1, y - 1, width + 2, height + 2, False, libtcod.BKGND_NONE)

    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (on main hand)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (on off hand)'.format(item.name))
            else:
                options.append(item.name)

    menu(con, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, screen_width, screen_height):
    libtcod.console_clear(0)

    libtcod.console_set_default_foreground(con, libtcod.light_fuchsia)

    foregroundLayer(screen_width, screen_height)

    # libtcod.console_print_frame(0,0,0,screen_width,screen_height,True,libtcod.BKGND_NONE)

    # libtcod.console_print_ex(con, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
    #                         'Cavern')
    libtcod.console_print_ex(con, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
                             'By ODST')

    menu(con, '', ['Play a new game', 'Continue', 'Quit'], 24, screen_width, screen_height)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution +20 HP from {0}'.format(player.fighter.max_hp),
               'Strength (+1 Attack from {0})'.format(player.fighter.power),
               'Agility (+1 Defense from {0})'.format(player.fighter.defense)]
    menu(con, header, options, menu_width, screen_width, screen_height)


def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character Information')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Level: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience: {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience to next Level: {0}'.format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 5, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Strength: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Agility: {0}'.format(player.fighter.defense))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'HP: {0}'.format(player.fighter.hp))

    x = int(screen_width/2) - int(character_screen_width/2)
    y = int(screen_height/2) - int(character_screen_height/2)
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height,0, x, y, 1.0, 0.7)




def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)
