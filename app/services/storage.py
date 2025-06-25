import os
import uuid
from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile
import logging
from datetime import datetime

load_dotenv()

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "uploads")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    logger.error(f"Supabase client initialization failed: {str(e)}")
    raise

async def upload_file_to_supabase(file: UploadFile) -> str:
    """Upload file to Supabase storage and return public URL"""
    try:
        # Generate unique filename with timestamp
        file_ext = file.filename.split(".")[-1].lower()
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        unique_filename = f"{timestamp}_{uuid.uuid4()}.{file_ext}"
        
        # Read file content
        file_content = await file.read()
        
        # Upload file with timeout
        upload_response = supabase.storage.from_(SUPABASE_BUCKET).upload(
            file=unique_filename,
            path=unique_filename,
            file_options={
                "content-type": file.content_type,
                "x-upsert": "true"
            }
        )
        
        if isinstance(upload_response, dict) and upload_response.get('error'):
            raise Exception(upload_response['error'])
        
        # Get public URL
        url_response = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(unique_filename)
        
        # Store metadata
        await store_file_metadata(unique_filename, file.filename, len(file_content))
        
        return url_response
    except Exception as e:
        logger.error(f"Supabase upload error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )

async def store_file_metadata(file_id: str, original_name: str, size: int):
    """Store file metadata in Supabase database"""
    try:
        response = supabase.table('file_metadata').insert({
            "file_id": file_id,
            "original_name": original_name,
            "size": size,
            "uploaded_at": "now()"
        }).execute()
        
        if hasattr(response, 'error') and response.error:
            logger.error(f"Error storing metadata: {response.error}")
    except Exception as e:
        logger.error(f"Metadata storage error: {str(e)}")
