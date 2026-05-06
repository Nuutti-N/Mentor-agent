
from supabase import create_client, Client
from config import settings

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def save_memory(content):
    supabase.table("memories").insert({"content": content}).execute()


def search_memories(query):
    result = supabase.table("memories").select(
        "*").ilike("content", f"%{query}%").execute()
    return result.data
