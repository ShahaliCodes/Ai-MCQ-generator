import openai
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_text_with_prompt(prompt: str, model: str = "gpt-3.5-turbo", **kwargs) -> str:
    """
    Generate text using OpenAI's API with the given prompt
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error in OpenAI API call: {str(e)}")
        raise

def format_questions_for_prompt(questions: List[Dict[str, Any]]) -> str:
    """
    Format questions into a string suitable for an AI prompt
    """
    formatted = []
    for q in questions:
        options = "\n".join([f"{opt['id']}) {opt['text']}" for opt in q['options']])
        formatted.append(
            f"Question: {q['text']}\n"
            f"Options:\n{options}\n"
            f"Correct Answer: {q['correct_answer']}\n"
            f"Explanation: {q['explanation']}\n"
        )
    return "\n".join(formatted)

def calculate_max_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a text string
    """
    # Rough estimate: 1 token ~= 4 characters
    return len(text) // 4