# app/utils/genai_chat.py
import json
import google.generativeai as genai

def setup_genai():
    genai.configure(api_key="AIzaSyCXg3hNjnOmJYaVJozUeAfINDZqD-UWfCk")  # Secure this!
    return genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')

def get_doctor_reply(model, user_message: str) -> str:
    prompt = f"""
    You are a helpful virtual doctor. A user has asked the following question:

    "{user_message}"

    Please provide a medically-informed and friendly response, especially for child care and baby nutrition.
    Limit your response to 150 words.
    """
    response = model.generate_content(prompt)
    return response.text.strip()
