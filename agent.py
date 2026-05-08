from google import genai
from google.genai.types import GenerateContentConfig
from config import settings
from memory import save_memory, search_memories

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def agent(message: str, history: list):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=history + [{"role": "user", "parts": [{"text": message}]}],
        config=GenerateContentConfig(
            tools=[save_memory, search_memories],
            system_instruction=[
                """ You are a brutal honest cofounder: your job is to
                Challenge bad ideas directly,
                Give feedback, if I make something so wrong or you have better way make,
                Give clear plan for me what should be do and why should be do,
                Ask for hard questions, what I avoiding,
                Just give examples and give plan what give me to chance to get job.

                Save any task, comment, or what I just tell for your!
                """
            ]
        )
    )
    return response.text
