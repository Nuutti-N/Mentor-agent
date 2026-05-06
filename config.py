from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    # Supabase
    SUPABASE_KEY: str
    SUPABASE_URL: str

    # Gemini
    GEMINI_API_KEY: str


settings = Settings()
