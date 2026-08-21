import asyncio
from dataclasses import dataclass


@dataclass
class Player:
    snake: Snake
    connector: asyncio.Queue

@dataclass
class Snake:
    pass


