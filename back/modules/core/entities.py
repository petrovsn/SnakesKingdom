import asyncio
from dataclasses import dataclass
import enum
from uuid import UUID
from typing import Any

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

class Snake:
    def __init__(self, snake_id, position, 
                 on_move_head = lambda id,pos:None, 
                 on_move_tail = lambda id,pos:None):
        self.id = snake_id
        self.hp =  4
        self.is_alive = True
        self.direction: Direction = Direction.ZERO
        self.next_direction: Direction = Direction.ZERO
        self.body = [position]

        

        self.on_move_head = on_move_head
        self.on_move_tail = on_move_tail

        self.on_move_head(self.id, self.get_head())

    def is_alive_check(func):
        def wrapper(self, *args, **kwargs):
            if self.is_alive:
                return func(self, *args, **kwargs)
        return wrapper

    def is_moving_check(func):
        def wrapper(self, *args, **kwargs):
            if self.next_direction != 0:
                return func(self, *args, **kwargs)
        return wrapper

    
    @is_alive_check
    def set_direction(self, new_direction:Direction):
        if ((self.direction+new_direction)%2==1) or (self.direction==0):
            self.next_direction = new_direction

    @is_alive_check
    @is_moving_check
    def move_head(self):
        self.direction = self.next_direction
        head = self.direction.apply(self.body[-1])
        self.body.append(head)
        self.on_move_head(self.id, head)

    @is_alive_check
    @is_moving_check
    def move_tail(self):
        self.direction = self.next_direction
        while len(self.body)>self.hp:
            tail = self.body.pop(0)
            self.on_move_tail(self.id, tail)

    @is_alive_check
    @is_moving_check
    def move(self):
        self.direction = self.next_direction
        while len(self.body)>=self.hp:
            tail = self.body.pop(0)
            self.on_move_tail(self.id, tail)

        head = self.direction.apply(self.body[-1])
        self.body.append(head)
        self.on_move_head(self.id, head)

    def get_head(self):
        return self.body[-1]

    def change_hp(self, value):
        self.hp+=value

    def death(self):
        self.is_alive = False
        self.body.pop(-1)

    def respawn(self, position):
        self.hp =  4
        self.is_alive = True
        self.direction: Direction = Direction.ZERO
        self.next_direction: Direction = Direction.ZERO
        self.body = [position]
        self.on_move_head(self.id, self.get_head())


@dataclass
class Participant:
    name: str
    color: str
    points: int = 0
    is_ready: bool = False

    def to_dict(self):
        return {
            "name":self.name,
            "color": self.color,
            "points": self.points,
            "is_ready": self.is_ready
        }

    def change_points(self, value):
        self.points+=value

@dataclass
class Player(Participant):
    connector: asyncio.Queue = None

@dataclass
class Bot(Participant):
    is_ready: bool = True
    ai: Any = lambda x: None
