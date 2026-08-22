import asyncio
from modules.core.game_engine import GameRoom

class GameManager:
    def __init__(self):
        self.rooms = {}

    def create_room(self, shape, speed, n_bots, respawn):
        new_room = GameRoom(shape, speed, n_bots, respawn)
        room_id = new_room.room_id
        asyncio.create_task(new_room.game_loop())
        self.rooms[room_id] = new_room
        return room_id

    def close_room(self, room_id):
        room = self.get_room(room_id)
        room.stop()

    def get_room(self, room_id):
        return self.rooms.get(room_id, None)