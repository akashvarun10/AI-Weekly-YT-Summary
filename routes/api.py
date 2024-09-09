# routes/api.py
from fastapi import APIRouter, BackgroundTasks
from models.user import User
from controllers.user_controller import subscribe, get_user, unsubscribe, get_all_users
from services.youtube_service import fetch_channels


router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to the YouTube Summary API"}

@router.post("/subscribe")
async def subscribe_route(user: User, background_tasks: BackgroundTasks):
    return await subscribe(user, background_tasks)

@router.get("/users/{email}")
async def get_user_route(email: str):
    return await get_user(email)

@router.get("/fetch_channels")
# async def fetch_channels_route(query: str):
#     return await fetch_channels(query)
async def fetch_channels_route(query: str):
    return fetch_channels(query) 

@router.get("/users")
async def get_all_users_route():
    return await get_all_users()

@router.get("/unsubscribe")
async def unsubscribe_route(email: str):
    return await unsubscribe(email)

