import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.services.file_processing import process_uploaded_file
from app.services.question_generation import generate_questions_from_content
from app.services.storage import upload_file_to_supabase
from app.schemas import QuestionSet
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="AI MCQ Generator API",
    description="API for generating MCQs from uploaded files using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/upload/", response_model=QuestionSet)
async def upload_file(file: UploadFile = File(...)):
    try:
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size is {max_size/1024/1024}MB"
            )

        logger.info(f"Processing file: {file.filename}")
        
        # 1. Upload file to Supabase storage
        file_url = await upload_file_to_supabase(file)
        logger.info(f"File uploaded to: {file_url}")
        
        # 2. Process file and extract text content
        content = await process_uploaded_file(file)
        logger.info(f"Extracted content length: {len(content)}")
        
        if not content or len(content.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from the file"
            )
        
        # 3. Generate questions from content
        questions = await generate_questions_from_content(content)
        logger.info(f"Generated {len(questions)} questions")
        
        return {
            "file_url": file_url,
            "questions": questions,
            "original_filename": file.filename
        }
    except HTTPException as he:
        logger.error(f"HTTP error: {he.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
