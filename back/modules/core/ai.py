from collections import deque
import random
from modules.core.entities import Direction
from modules.core.maps.game_map import GameMap
from modules.core.maps.tiles import Tile
from modules.core.snake_collider import SnakesCollisionController
from modules.core.pathfinding import PathFinder, PF_Algorithms

class BotAi:
    def __init__(self, game_map: GameMap, snake_collisions_controller: SnakesCollisionController):
        self.game_map = game_map
        self.pf: PathFinder = PathFinder(game_map, snake_collisions_controller)
        self.pf.mode = random.choice(list(PF_Algorithms))

    def get_direction(
        self,
        head_position: tuple):
        food_pos = self._find_food(head_position)

        not_decision_direction = self.pf.get_safe_direction(head_position)

        if food_pos is None:
            return not_decision_direction
        
        direction = self.pf.find_path(head_position,food_pos)

        if direction is not None:
            return direction

        return not_decision_direction

    def _find_food(self, from_position):
        food_pos = self.game_map.get_closest_tile(from_position, Tile.FOOD)
        return food_pos
