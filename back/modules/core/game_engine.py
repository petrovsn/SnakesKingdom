import time
from modules.core.entities import Snake, Player, Tile
import asyncio
from uuid import uuid4


class GameRoom:
    def __init__(self, shape: tuple = (10,10), n_bots: int = 0):
        self.map: list[list[int]] = [[0]*shape[0]]*shape[1]

        self.snaked_tiles = {

        }

        self.players: dict[int,Player] = {}
        self.mobs:dict[int,Snake] = {}
        self.active = True

    def add_player(self) -> int:
        player_id = uuid4().hex
        self.players[player_id] = Player(
            snake = Snake(),
            connector=asyncio.Queue(maxsize=1)
        )
        return player_id

    def remove_player(self,player_id):
        self.players.pop(player_id)

    def add_mob(self):
        pass

    def stop(self):
        self.active = False

    def handle_command(self, player_id, direction):
        self.players[player_id].snake.set_direction(direction)


    def on_head_collision(self, snake:Snake, head_position):
        x,y = head_position
        match self.map[x][y]:
            case Tile.FOOD:
                snake.change_hp(1)
            case Tile.WALL:
                snake.death()

    def update_world(self):
        for player in self.players.values():
            player.snake.move_head()


        for player in self.players.values():
            player.snake.move_tail()

    def get_game_data(self, player_id):
        return {
            "player_id":str(player_id),
            "world":self.map
        }

    def update_views(self):
        for player_id, player in self.players.items():
            game_data = self.get_game_data(player_id)

            if player.connector.full():
                player.connector.get_nowait()

            player.connector.put_nowait(game_data)

    async def game_loop(self):
        while self.active:
            time_start = time.perf_counter()

            self.update_world()

            self.update_views()

            time_end = time.perf_counter()
            exec_time = time_end-time_start
            await asyncio.sleep(1-exec_time)

    def get_data_connector(self, player_id):
        return self.players[player_id].connector



class GameManager:
    def __init__(self):
        self.rooms = {}

    def create_room(self):
        new_room = GameRoom()
        room_id = uuid4().hex
        asyncio.create_task(new_room.game_loop())
        self.rooms[room_id] = new_room
        return room_id


    def close_room(self, room_id):
        room = self.get_room(room_id)
        room.stop()

    def get_room(self, room_id):
        return self.rooms.get(room_id, None)