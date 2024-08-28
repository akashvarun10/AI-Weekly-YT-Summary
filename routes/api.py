# routes/api.py
from fastapi import APIRouter, BackgroundTasks
from models.user import User
from controllers.user_controller import subscribe, get_user
from services.youtube_service import fetch_channels

router = APIRouter()

@router.post("/subscribe")
async def subscribe_route(user: User, background_tasks: BackgroundTasks):
    return await subscribe(user, background_tasks)

@router.get("/users/{email}")
async def get_user_route(email: str):
    return await get_user(email)

@router.get("/fetch_channels")
async def fetch_channels_route(query: str):
    return await fetch_channels(query)