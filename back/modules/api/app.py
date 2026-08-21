from fastapi import FastAPI
import asyncio
from modules.api.routes.game import game_router
from modules.api.routes.admin import admin_router
from contextlib import asynccontextmanager
from modules.core.game_engine import GameManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    game_manager = GameManager()
    app.state.game_manager =game_manager

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(game_router)
app.include_router(admin_router)