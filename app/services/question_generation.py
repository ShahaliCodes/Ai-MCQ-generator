import os
import openai
import random
import logging
from typing import List
from app.schemas import Question, QuestionOption
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_questions_from_content(content: str, num_questions: int = 20) -> List[Question]:
    """Generate MCQs from extracted content using OpenAI API"""
    try:
        if not content or len(content.strip()) < 50:
            raise ValueError("Content is too short to generate questions")
        
        # Split content into chunks if too large
        content_chunks = _split_content(content)
        
        questions = []
        for chunk in content_chunks:
            if len(questions) >= num_questions:
                break
                
            prompt = f"""
            Based on the following content, generate multiple-choice questions with 4 options each. 
            Each question should have one correct answer and three plausible but incorrect answers.
            Format each question exactly as follows:
            
            Question: [question text]
            Options:
            A) [option 1]
            B) [option 2]
            C) [option 3]
            D) [option 4]
            Correct Answer: [letter of correct option]
            Explanation: [brief explanation why this is correct]
            
            Content:
            {chunk}
            """
            
            response = await _call_openai_api(prompt)
            
            generated_text = response.choices[0].message.content
            parsed_questions = _parse_generated_questions(generated_text)
            questions.extend(parsed_questions)
        
        # Randomize and limit to requested number of questions
        random.shuffle(questions)
        return questions[:num_questions]
    except Exception as e:
        logger.error(f"Error generating questions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate questions: {str(e)}"
        )

async def _call_openai_api(prompt: str):
    """Wrapper for OpenAI API call with error handling"""
    try:
        return await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates educational multiple-choice questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise Exception(f"OpenAI API error: {str(e)}")

def _split_content(content: str, max_chunk_size: int = 2000) -> List[str]:
    """Split content into manageable chunks for the API"""
    words = content.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(word)
        current_length += len(word) + 1
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def _parse_generated_questions(text: str) -> List[Question]:
    """Parse the generated text into structured questions"""
    questions = []
    current_question = None
    current_options = []
    current_correct = None
    current_explanation = None
    
    lines =