import os
import uuid
from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile
import logging

load_dotenv()

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "uploads")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def upload_file_to_supabase(file: UploadFile) -> str:
    """Upload file to Supabase storage and return public URL"""
    try:
        # Generate unique filename
        file_ext = file.filename.split(".")[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        
        # Read file content
        file_content = await file.read()
        
        # Upload file
        res = supabase.storage.from_(SUPABASE_BUCKET).upload(
            unique_filename, 
            file_content,
            content_type=file.content_type
        )
        
        if isinstance(res, dict) and res.get('error'):
            raise Exception(res['error'])
        
        # Get public URL
        url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(unique_filename)
        
        # Store metadata
        await store_file_metadata(unique_filename, file.filename, len(file_content))
        
        return url
    except Exception as e:
        logger.error(f"Supabase upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )

async def store_file_metadata(file_id: str, original_name: str, size: int):
    """Store file metadata in Supabase database"""
    try:
        res = supabase.table('file_metadata').insert({
            "file_id": file_id,
            "original_name": original_name,
            "size": size
        }).