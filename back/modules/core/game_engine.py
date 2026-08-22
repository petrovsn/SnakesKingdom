import time
import asyncio
from uuid import uuid4
from modules.core.entities import Snake, Player, Direction, Bot, Participant
from modules.core.map_generator import GameMap, Tile
from modules.core.snake_collider import SnakesCollisionController

from modules.utils.colors import get_color

class GameRoom:
    def __init__(self, shape: tuple = (20,20), speed = 4, n_bots: int = 0, respawn = True):
        self.game_tick = 1.0/speed
        self.map: GameMap = GameMap(shape)
        self.snake_collision_controller = SnakesCollisionController()
        random_empty_position = self.map.get_random_free_place(on_additional_check = self.snake_collision_controller.is_not_snaked)
        self.map.place_object(random_empty_position, Tile.FOOD)

        self.participants: dict[str, Participant] = {}
        self.snakes: dict[str, Snake] = {}

        self.active = False

        self.respawn = respawn
        self._room_id = uuid4().hex

    @property
    def room_id(self):
        return self._room_id


    def add_player(self) -> int:
        player_id = uuid4().hex
        player_color = get_color(player_id)
        self.participants[player_id] = Player(
            name="UnknownPlayer",
            connector=asyncio.Queue(maxsize=1),
            is_ready = self.active,
            color=player_color
        )

        free_position = self.map.get_random_free_place()
        self.snakes[player_id] = Snake(snake_id = player_id,
                                       position=free_position, 
                                       on_move_head=self.snake_collision_controller.claim,
                                       on_move_tail=self.snake_collision_controller.free)
        return player_id

    def name_player(self, player_id, player_name):
        self.participants[player_id].name = player_name

    def remove_player(self,player_id):
        self.participants.pop(player_id)
        self.snakes.pop(player_id)
        self.snake_collision_controller.free_from(player_id)

    def players_are_ready(self):
        result = True
        for participant in self.participants.values():
            result = result and participant.is_ready
        return result

    def stop(self):
        self.active = False

    def handle_command(self, snake_id, command):
        if command == "ready":
            self.participants[snake_id].is_ready = True
        elif command == "respawn":
            if self.respawn and not self.snakes[snake_id].is_alive:
                self.snakes[snake_id].respawn()
        else:
            try:
                direction = getattr(Direction, command.upper())
                self.snakes[snake_id].set_direction(direction)
            except AttributeError as e:
                print("wrong command")


    def update_snake_movement(self):
        for snake in self.snakes.values():
            snake.move()

    def check_world_collisions(self):
        for snake_id, snake in self.snakes.items():
            head_position = snake.get_head()
            match self.map.get_item(head_position):
                case Tile.FOOD:
                    snake.change_hp(1)
                    self.map.place_object(head_position, Tile.EMPTY)
                    random_empty_position = self.map.get_random_free_place(on_additional_check = self.snake_collision_controller.is_not_snaked)
                    self.map.place_object(random_empty_position, Tile.FOOD)
                    self.participants[snake_id].change_points(1)

                case Tile.WALL:
                    self.participants[snake_id].change_points(-1)
                    snake.death()

    def check_snakes_collisions(self):
        collided_snakes = self.snake_collision_controller.get_collided_snakes()
        for snake_id in collided_snakes:
            self.snakes[snake_id].death()
            self.participants[snake_id].change_points(-1)
        self.snake_collision_controller.next_step()

    def update_bots_directions(self):
        pass

    def update_world(self):
        self.update_snake_movement()
        self.check_world_collisions()
        self.check_snakes_collisions()
        self.update_bots_directions()

    def serialize_snake(self, snake_id):
        snake = self.snakes.get(snake_id)
        return {
            "hp": snake.hp,
            "color": self.participants[snake.id].color,
            "alive": snake.is_alive,
            "direction": snake.direction.value,
            "body": snake.body,
        }

    def get_game_data(self, player_id):
        return {
            "player_id":player_id,
            "service_info":{
                "room_id": self.room_id,
                "speed": 1/self.game_tick,
                "respawn": self.respawn,
                "participants": [participant.to_dict() for participant in self.participants.values()],
                "timestamp": self.snake_collision_controller.current_timestamp
            },
            "snakes": {
                snake_id: self.serialize_snake(snake_id) for snake_id in self.snakes
            },
            "world":self.map.get_data(),
        }

    def update_views(self):
        for player_id, player in self.participants.items():
            if isinstance(player, Player):
                game_data = self.get_game_data(player_id)

                if player.connector.full():
                    player.connector.get_nowait()

                player.connector.put_nowait(game_data)

    async def game_loop(self):
        while not self.players_are_ready():
            await asyncio.sleep(0.1)

        self.active = True
        while self.active:
            time_start = time.perf_counter()

            self.update_world()

            self.update_views()

            time_end = time.perf_counter()
            exec_time = time_end-time_start
            await asyncio.sleep(max(0,self.game_tick-exec_time))

    def get_data_connector(self, player_id):
        return self.participants[player_id].connector