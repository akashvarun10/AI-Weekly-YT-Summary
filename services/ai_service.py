# services/ai_service.py
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.schema import HumanMessage
from config.settings import settings
import logging
import openai 
import anthropic

genai.configure(api_key=settings.GOOGLE_API_KEY)
openai.api_key = settings.OPENAI_API_KEY
anthropic.api_key = settings.ANTHROPIC_API_KEY

def extract_transcript_details_and_generate_summary(youtube_video_url: str) -> tuple:
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])

        # Try Gemini first
        try:
            model = genai.GenerativeModel("gemini-pro")
            prompt = f"Summarize the following YouTube video transcript:\n\n{transcript}"
            response = model.generate_content(prompt)
            return response.text, "Gemini"
        except Exception as gemini_error:
            logging.error(f"Gemini error: {gemini_error}")

        # If Gemini fails, try OpenAI
        try:
            chat = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=settings.OPENAI_API_KEY)
            response = chat([HumanMessage(content=f"Summarize the following YouTube video transcript:\n\n{transcript}")])
            return response.content, "OpenAI (GPT-4o-mini)"
        except Exception as openai_error:
            logging.error(f"OpenAI error: {openai_error}")

        # If OpenAI fails, try Anthropic
        try:
            chat = ChatAnthropic(model="claude-3-5-sonnet-20240620", anthropic_api_key=settings.ANTHROPIC_API_KEY)
            response = chat([HumanMessage(content=f"Summarize the following YouTube video transcript:\n\n{transcript}")])
            return response.content, "Anthropic (Claude-3-5-Sonnet)"
        except Exception as anthropic_error:
            logging.error(f"Anthropic error: {anthropic_error}")

        # If all methods fail, return an error message
        return "Unable to generate summary due to API issues. Please try again later.", "None"

    except Exception as e:
        logging.error(f"Error in extract_transcript_details_and_generate_summary: {e}")
        return f"An error occurred: {e}", "None"
