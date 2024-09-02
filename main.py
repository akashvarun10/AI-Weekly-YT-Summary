import logging
import threading
import time
import schedule
import asyncio
from fastapi import FastAPI
from routes.api import router
from services.email_service import send_email
from services.youtube_service import get_channel_id, get_latest_video_url
from services.ai_service import extract_transcript_details_and_generate_summary
from controllers.user_controller import users_collection
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Or specify allowed methods
    allow_headers=["*"],  # Or specify allowed headers
)

async def weekly_update():
    logging.info("Starting weekly update")
    users = await users_collection.find().to_list(None)
    for user in users:
        summaries = []
        for channel_name in user["channels"]:
            channel_id = get_channel_id(channel_name)
            if channel_id:
                video_url = get_latest_video_url(channel_id)
                if video_url:
                    summary, model_used = extract_transcript_details_and_generate_summary(video_url)
                    summaries.append(f"Channel: {channel_name}\nVideo: {video_url}\nSummary: {summary}\nSummarized by: {model_used}\n\n")

        if summaries:
            email_body = "Here are your weekly YouTube channel summaries:\n\n" + "\n".join(summaries)
            send_email(user["email"], "Weekly YouTube Channel Summaries", email_body)
            logging.info(f"Sent weekly summary to {user['email']}")
    logging.info("Completed weekly update")

@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    schedule.every().sunday.at("21:05").do(lambda: asyncio.run_coroutine_threadsafe(weekly_update(), loop))
    logging.info("Scheduled weekly update for Sundays at 20:40 (ET)")

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
    logging.info("Started scheduler thread")

if __name__ == "__main__":
    import uvicorn
    logging.info("Starting the FastAPI application")
    uvicorn.run(app, host="0.0.0.0", port=8000)