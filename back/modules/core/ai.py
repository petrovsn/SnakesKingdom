from collections import deque

from modules.core.entities import Direction
from modules.core.map_generator import GameMap, Tile
from modules.core.snake_collider import SnakesCollisionController


class BotAi:
    def __init__(self):
        pass

    def get_direction(
        self,
        head_position: tuple,
        map: GameMap,
        snake_collision_controller: SnakesCollisionController,
    ):
        food = self._find_food(head_position, map)

        if food is None:
            return self._get_safe_direction(
                head_position,
                map,
                snake_collision_controller,
            )

        direction = self._find_path(
            head_position,
            food,
            map,
            snake_collision_controller,
        )

        if direction is not None:
            return direction

        return self._get_safe_direction(
            head_position,
            map,
            snake_collision_controller,
        )

    def _find_food(self, from_position, map: GameMap):
        food_pos = map.get_closest_tile(from_position, Tile.FOOD)
        return food_pos

    def _find_path(
        self,
        start,
        target,
        map,
        snake_collision_controller,
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
                    map,
                    snake_collision_controller,
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

    def _get_safe_direction(
        self,
        head_position,
        map,
        snake_collision_controller,
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
                position,
                map,
                snake_collision_controller,
            ):
                return direction

        return Direction.ZERO

    def _is_safe(
        self,
        position,
        map,
        snake_collision_controller:SnakesCollisionController,
    ):
        try:
            tile = map.get_item(position)
        except (IndexError, TypeError):
            return False

        if tile == Tile.WALL:
            return False

        return snake_collision_controller.is_not_snaked(
            position
        )