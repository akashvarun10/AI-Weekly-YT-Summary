from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException, BackgroundTasks
from models.user import User
from services.email_service import send_welcome_email
import logging
from config.settings import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client["youtube_summary_app"]
users_collection = db["users"]

async def subscribe(user: User, background_tasks: BackgroundTasks):
    try:
        existing_user = await users_collection.find_one({"email": user.email})
        if existing_user:
            await users_collection.update_one({"email": user.email}, {"$set": {"channels": user.channels}})
            message = "Subscription updated successfully"
            logging.info(f"Updated subscription for user: {user.email}")
        else:
            await users_collection.insert_one(user.dict())
            message = "Subscription created successfully"
            logging.info(f"Created new subscription for user: {user.email}")
            background_tasks.add_task(send_welcome_email, user.email, user.channels)
        return {"message": message}
    except Exception as e:
        logging.error(f"Error in subscribe: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_user(email: str):
    try:
        user = await users_collection.find_one({"email": email})
        if user:
            return {"email": user["email"], "channels": user["channels"]}
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logging.error(f"Error in get_user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

