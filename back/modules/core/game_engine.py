from modules.core.game_rooms.game_room_core import GameRoom
from modules.core.game_rooms.game_room_obstacled import GameRoomObstacled

class GameEngine:
    room_classes = {
        "classic": GameRoom,
        "obstacled": GameRoomObstacled
    }

    @staticmethod
    def get_room(room_type, *args, **kwargs):
        if room_type in GameEngine.room_classes:
            return GameEngine.room_classes[room_type](*args, **kwargs)