import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-3.5-flash")


def ask_gemini(prompt: str):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"