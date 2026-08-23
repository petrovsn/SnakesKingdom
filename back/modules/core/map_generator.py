import enum
import random

class Tile(int, enum.Enum):
    EMPTY = 0
    SNAKE = 1
    FOOD = 2
    WALL = 3
    NEST = 4

class MapGenerator:
    def __init__(self):
        pass

    def get_new_map(shape:tuple, mode = "simple"):
        pass

"""
  [1,1,1,1,1,1,1]
  [1,0,0,1,0,0,1]
y3[1, 0,0,1,0,0,1]
y1[1,0,0,0,0,0,1]
y0[1,1,1,1,1,1,1]
x0 x1 x2
"""

class GameMap:
    def __init__(self,shape:tuple):
        x,y = shape
        self.shape = shape
        self.map = []
        self.map = [[Tile.WALL]+[Tile.EMPTY for i in range(x)]+[Tile.WALL] for j in range(y)]
        self.map.append([Tile.WALL for _ in range(x + 2)])
        self.map.insert(0, [Tile.WALL for _ in range(x + 2)])
        self.last_added_tile = {}

    def get_random_free_place(
        self,
        on_additional_check=lambda pos: True,
        max_tries = 100
    ):
        for _ in range(max_tries):
            x_rand = random.randint(1, self.shape[0])
            y_rand = random.randint(1, self.shape[1])

            position = (x_rand, y_rand)

            if self.get_item(position) != Tile.EMPTY:
                continue

            if not on_additional_check(position):
                continue

            return position
        return None


    def get_closest_tile(self, position, tile: Tile):
        return self.last_added_tile.get(tile)
    
    def place_object(self, position: tuple, item: Tile):
        x,y = position
        self.map[y][x] = item
        self.last_added_tile[item] = (x,y)

    def get_item(self, position):
        x,y = position
        return self.map[y][x]

    def get_data(self):
        return self.map

    def _draw_(self):
        mapping = {
            Tile.EMPTY: " ",
            Tile.SNAKE: "S",
            Tile.WALL: "🧱",
            Tile.FOOD: "🍎",
            Tile.NEST: "O"
        }

        symbol_map = [
            "".join([mapping[tile] for tile in row]) for row in self.map[::-1]
        ]

        string_map = '\n'.join(symbol_map)

        return string_map