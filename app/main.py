import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.services.file_processing import process_uploaded_file
from app.services.question_generation import generate_questions_from_content
from app.services.storage import upload_file_to_supabase
from app.schemas import QuestionSet

load_dotenv()

app = FastAPI(
    title="AI MCQ Generator API",
    description="API for generating MCQs from uploaded files using AI",
    version="1.0.0"
)

# Correct CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-mcq-generator-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/", response_model=QuestionSet)
async def upload_file(file: UploadFile = File(...)):
    try:
        file_url = await upload_file_to_supabase(file)
        content = await process_uploaded_file(file)
        questions = await generate_questions_from_content(content)
        return {
            "file_url": file_url,
            "questions": questions,
            "original_filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "✅ AI MCQ Generator Backend is live!"}