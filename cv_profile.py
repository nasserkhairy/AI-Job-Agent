import json
from gemini_service import ask_gemini_json


def create_profile(cv_text):

    prompt = f"""
    Return VALID JSON ONLY.

    {{
      "name": "",
      "title": "",
      "years_experience": 0,
      "skills": []
    }}

    CV:
    {cv_text}
    """

    return ask_gemini_json(prompt)