import asyncio
from dataclasses import dataclass
import enum

class Tile(int, enum.Enum):
    EMPTY = 0
    SNAKE = 1
    FOOD = 2
    WALL = 3
    NEST = 4

class Direction(int, enum.Enum ):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    ZERO = 0

    def apply(self, position: tuple):
        x, y = position
        match self:
            case Direction.UP:
                return (x, y+1)
            case Direction.DOWN:
                return (x, y-1)
            case Direction.RIGHT:
                return (x+1, y)
            case Direction.LEFT:
                return (x-1, y)
            case Direction.ZERO:
                return (x, y)

"""
[1,1,1,1,1,1,1]
[1,0,0,1,0,0,1]
[1,0,0,1,0,0,1]
[1,0,0,0,0,0,1]
[1,1,1,1,1,1,1]
"""

class Snake:
    

    def __init__(self, position, 
                 on_move_head = lambda id,pos:None, 
                 on_move_tail = lambda id,pos:None):

        self.hp =  5
        self.direction: Direction = Direction.ZERO
        self.body = [position]
        self.on_move_head = on_move_head
        self.on_move_tail = on_move_tail

    def set_direction(self, new_direction:Direction):
        if ((self.direction+new_direction)%2==1) or (self.direction==0):
            self.direction = new_direction

    def move_head(self):
        if self.direction != 0:
            head = self.direction.apply(self.body[-1])
            self.body.append(head)
            self.on_move_head(self, head)

    def move_tail(self):
        while len(self.body)>self.hp:
            tail = self.body.pop(0)
            self.on_move_tail(self, tail)

    def change_hp(self, value):
        self.hp+=value

    def death(self):
        pass


@dataclass
class Player:
    snake: Snake
    connector: asyncio.Queue
