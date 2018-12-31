import random

def wallCreate():
    randomChance = random.randint(1, 100)
    if randomChance <= 40:
        return 1
    else:
        return 0

def printOutput(my_randoms):
    for i in my_randoms:
        levelString = ""
        for j in i:
            if j == 1:
                levelString += "#"
            else:
                levelString += " "


def cellular_automata_pass(my_randoms):
    new_randoms = my_randoms.copy()
    reproduceCount = 0

    for rowCount, row in enumerate(my_randoms):
        for colCount, column in enumerate(row):
            # print(colCount)
            # Reproducing occurs in empty tiles
            if (rowCount != 0 and rowCount != len(my_randoms) - 1 and colCount != 0 and colCount != len(row) - 1):

                for r in (-1, 0, 1):
                    for c in (-1, 0, 1):
                        if my_randoms[rowCount + r][colCount + c] == 1:
                            reproduceCount += 1

                if reproduceCount <= 4:
                    new_randoms[rowCount][colCount] = 0
                elif reproduceCount >= 5:
                    new_randoms[rowCount][colCount] = 1

                reproduceCount = 0

    return new_randoms


def get_cave_generated(map_width, map_height):
    my_randoms = [[wallCreate() for i in range(map_width)] for j in range(map_height)]

    for r in (-1, 0, 1):
        for c in (-1, 0, 1):
            my_randoms[int(map_height/2)+c][int(map_width/2)+r] = 0

    for i in range(1):
        my_randoms = cellular_automata_pass(my_randoms)

    printOutput(my_randoms)

    return my_randoms


def make_cave_room(self, room_width, room_height, room_x, room_y,map_width, map_height):
    generated_cave = get_cave_generated(room_width, room_height)
    for x, row in enumerate(generated_cave):
        for y, col in enumerate(row):
            if not (x+room_x < 0 or x+room_x >= map_width or y+room_y <0 or y+room_y >= map_height):
                if col == 1:
                    self.tiles[x+room_x][y+room_y].blocked = True
                    self.tiles[x+room_x][y+room_y].block_sight = True
                if col == 0:
                    self.tiles[x+room_x][y+room_y].blocked = False
                    self.tiles[x+room_x][y+room_y].block_sight = False
