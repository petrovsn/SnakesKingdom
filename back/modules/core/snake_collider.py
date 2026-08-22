import time
import asyncio
from uuid import uuid4

from modules.core.entities import Snake, Player, Direction
from modules.core.map_generator import GameMap, Tile

from collections import defaultdict

from dataclasses import dataclass

@dataclass
class TileClaim:
    snake_id: int
    timestamp: int

class SnakesCollisionController:
    def __init__(self):
        self.current_timestamp = 0
        self.snaked_tiles = {}
        self.collided_snakes = []

    def claim(self, snake_id, position:tuple):
        current_claim:TileClaim = self.snaked_tiles.get(position,None)
        if current_claim is None:
            self.snaked_tiles[position] = TileClaim(snake_id=snake_id, timestamp=self.current_timestamp)
        else:
            if current_claim.timestamp == self.current_timestamp:
                self.collided_snakes.append(current_claim.snake_id)
                self.collided_snakes.append(snake_id)
            else:
                self.collided_snakes.append(snake_id)

    def free(self, snake_id, position:tuple):
        if position in self.snaked_tiles:
            self.snaked_tiles.pop(position)

    def free_from(self, snake_id):
        to_delete = []
        for position, tile_claim in self.snaked_tiles.items():
            if tile_claim.snake_id == snake_id:
                to_delete.append(position)
        for position in to_delete:
            self.free(snake_id, position)

    def get_collided_snakes(self):
        return self.collided_snakes 

    def next_step(self):
        self.collided_snakes = []
        self.current_timestamp+=1

    def is_not_snaked(self, position):
        return position not in self.snaked_tiles