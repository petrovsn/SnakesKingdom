from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from modules.core.game_engine import GameManager, GameRoom
import asyncio

game_router = APIRouter(prefix="/game", tags=["ws"])

class PlayerConnection:
    def __init__(self, player_id, game_room:GameRoom, websocket:WebSocket):
        self.player_id = player_id
        self.game_room:GameRoom = game_room
        self.websocket:WebSocket = websocket

    async def send_game_data(self):
        connector: asyncio.Queue = self.game_room.get_data_connector(self.player_id)
        while True:
            game_data = await connector.get()
            await self.websocket.send_json(game_data)

    async def receive_commands(self):
        try:
            while True:
                message = await self.websocket.receive_json()
                print(f"messege received: {message}")
                self.game_room.handle_command(self.player_id, "mock")

        except WebSocketDisconnect:
            print("connection closed")


@game_router.websocket("/{game_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    game_id: str,
):
    await websocket.accept()

    game_manager:GameManager = websocket.app.state.game_manager
    game_room:GameRoom = game_manager.get_room(game_id)
    player_id = game_room.add_player()

    player_connection = PlayerConnection(player_id, game_room, websocket)

    receive_task = asyncio.create_task(
        player_connection.receive_commands()
    )

    send_task = asyncio.create_task(
        player_connection.send_game_data()
    )

    done, pending = await asyncio.wait(
        [receive_task, send_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

    await asyncio.gather(
        *pending,
        return_exceptions=True,
    )

    game_room.remove_player(player_id)


@game_router.post("/rooms")
async def create_room(request: Request):
    game_manager: GameManager = request.app.state.game_manager
    room_id = game_manager.create_room()
    return {
        "room_id": room_id
    }