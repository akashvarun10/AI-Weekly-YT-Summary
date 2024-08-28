# AI-Weekly YouTube Channel Summary Service
AI Weekly YT Summary Using Gemini, OpenAI, Claude.
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)![LangChain](https://img.shields.io/badge/LangChain-00BFFF?style=for-the-badge&logo=langchain&logoColor=white)![OpenAI](https://img.shields.io/badge/OpenAI-8C1D40?style=for-the-badge&logo=openai&logoColor=white)![Claude](https://img.shields.io/badge/Claude-00A3E0?style=for-the-badge&logo=anthropic&logoColor=white)![Gemini](https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white)![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)

This project provides a FastAPI-based service for summarizing YouTube channels. It encompasses several key components for handling user subscriptions, fetching YouTube data, generating summaries with AI, and sending email updates.

## Key Components

1. **Environment Configuration (`Settings` class)**:
   - Loads environment variables from a `.env` file using `dotenv`.
   - Includes API keys for MongoDB, SMTP, YouTube, OpenAI, and Anthropic.

2. **User Subscription Handling**:
   - **MongoDB Connection**: Connects to a `youtube_summary_app` database with a `users` collection.
   - **Subscription Logic**:
     - `subscribe`: Manages user subscriptions, updates existing ones, or creates new ones, and schedules a welcome email.
     - `get_user`: Retrieves user data by email.

3. **API Routes (`routes/api.py`)**:
   - `/subscribe`: Allows users to subscribe.
   - `/users/{email}`: Retrieves user data based on email.
   - `/fetch_channels`: Searches for YouTube channels based on a query.

4. **YouTube Service (`services/youtube_service.py`)**:
   - **`get_channel_id`**: Fetches YouTube channel IDs.
   - **`get_latest_video_url`**: Retrieves the latest video URL for a channel.
   - **`fetch_channels`**: Searches for channels based on a query.

5. **AI Service (`services/ai_service.py`)**:
   - Extracts video transcripts and summarizes them using `Gemini, OpenAI GPT-4, or Anthropic Claude. Returns an error message if summarization fails.

6. **Email Service (`services/email_service.py`)**:
   - **`send_email`**: Handles sending emails via SMTP.
   - **`send_welcome_email`**: Sends a welcome email listing subscribed channels.

7. **Weekly Update Function (`main.py`)**:
   - **`weekly_update`**: Runs every Wednesday at 10:43 AM, fetching and emailing the latest video summaries to all users.
   - **Scheduler**: A background thread manages the scheduling for weekly updates.

8. **Startup Event**:
   - Triggers on FastAPI application startup to schedule weekly updates and start the scheduler thread.

This service automates user subscriptions to YouTube channels, provides weekly video summaries, and utilizes various AI models for content summarization, all while managing user data and notifications efficiently.