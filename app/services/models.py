from typing import Optional
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

class FileMetadata:
    """Model for storing file metadata in Supabase"""
    @staticmethod
    async def create(file_id: str, original_name: str, size: int):
        response = supabase.table('file_metadata').insert({
            "file_id": file_id,
            "original_name": original_name,
            "size": size
        }).execute()
        
        if response.data:
            return response.data[0]
        return None

    @staticmethod
    async def get(file_id: str):
        response = supabase.table('file_metadata').select("*").eq("file_id", file_id).execute()
        if response.data:
            return response.data[0]
        return None