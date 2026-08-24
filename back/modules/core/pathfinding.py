from modules.core.entities import Direction
from modules.core.snake_collider import SnakesCollisionController
from modules.core.maps.game_map import GameMap
from modules.core.maps.tiles import Tile
import random
from collections import deque
import enum
from modules.utils.distance import get_distance

class PF_Algorithms(str, enum.Enum):
    BFS = "bfs"
    GREEDY = "greedy"


class PathFinder:
    def __init__(self, game_map:GameMap, snake_collision_controller: SnakesCollisionController):
        self.game_map:GameMap = game_map
        self.snake_collision_controller:SnakesCollisionController = snake_collision_controller
        self.mode:PF_Algorithms = PF_Algorithms.GREEDY

    def find_path(
            self,
            start,
            target
        ):
        match self.mode:
            case PF_Algorithms.GREEDY:
                return self._find_path_greedy(start,target)
            case PF_Algorithms.BFS:
                return self._find_path_BFS(start, target)
        return None

    def _is_safe(
        self,
        position,
    ):
        try:
            tile = self.game_map.get_tile(position)
        except (IndexError, TypeError):
            return False

        if tile == Tile.WALL:
            return False

        return self.snake_collision_controller.is_not_snaked(
            position
        )

    def get_safe_direction(
        self,
        head_position,
    ):
        directions = (
            (Direction.UP, (0, 1)),
            (Direction.RIGHT, (1, 0)),
            (Direction.DOWN, (0, -1)),
            (Direction.LEFT, (-1, 0)),
        )

        for direction, (dx, dy) in directions:
            position = (
                head_position[0] + dx,
                head_position[1] + dy,
            )

            if self._is_safe(
                position
            ):
                return direction

        return Direction.ZERO

    def _find_path_greedy(
            self,
            start,
            target
        ):
        directions = (
            (Direction.UP, (0, 1)),
            (Direction.RIGHT, (1, 0)),
            (Direction.DOWN, (0, -1)),
            (Direction.LEFT, (-1, 0)),
        )


        candidates = {}

        for direction, (dx, dy) in directions:
            position = (
                start[0] + dx,
                start[1] + dy,
            )

            if not self._is_safe(
                position
            ):
                continue

            distance = get_distance(position, target)

            candidates[direction] = distance

        if candidates != {}:
            min_value = min(candidates.values())
            candidates = [k for k, v in candidates.items() if v == min_value]
            return random.choice(candidates)
        return Direction.ZERO

    def _find_path_BFS(
        self,
        start,
        target,
    ):
        queue = deque()
        queue.append(start)

        visited = {start}

        first_direction = {}

        directions = (
            (Direction.UP, (0, 1)),
            (Direction.RIGHT, (1, 0)),
            (Direction.DOWN, (0, -1)),
            (Direction.LEFT, (-1, 0)),
        )

        while queue:
            current = queue.popleft()

            if current == target:
                return first_direction.get(current)

            for direction, (dx, dy) in directions:
                next_position = (
                    current[0] + dx,
                    current[1] + dy,
                )

                if next_position in visited:
                    continue

                if not self._is_safe(
                    next_position,
                ):
                    continue

                visited.add(next_position)

                if current == start:
                    first_direction[next_position] = direction
                else:
                    first_direction[next_position] = \
                        first_direction[current]

                queue.append(next_position)

        return None