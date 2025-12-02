from pathlib import Path
from google import genai
from app.config import settings


class LLMServiceError(Exception):
    """Custom exception for LLM service errors."""
    pass

client = genai.Client(api_key=settings.GOOGLE_API_KEY)
MODEL = "gemini-2.0-flash"

PROMPTS_DIR = Path(__file__).parent.parent / "system_prompts"


def _load_prompt(filename: str) -> str:
    """Load a prompt template from the system_prompts folder."""
    path = PROMPTS_DIR / filename
    return path.read_text(encoding="utf-8")


def generate_essay_prompt(text: str) -> str:
    template = _load_prompt("generate_essay.txt")
    prompt = template.format(text=text)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[prompt]
        )
        return response.text.strip()
    except Exception as e:
        raise LLMServiceError(f"Failed to generate essay prompt: {str(e)}")

def generate_mcqs(text: str) -> str:
    template = _load_prompt("generate_mcq.txt")
    prompt = template.format(text=text)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[prompt]
        )
        return response.text.strip()
    except Exception as e:
        raise LLMServiceError(f"Failed to generate MCQs: {str(e)}")

def grade_essay(text: str, prompt: str, user_answer: str) -> str:
    template = _load_prompt("grade_essay.txt")
    grading_prompt = template.format(text=text, prompt=prompt, user_answer=user_answer)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[grading_prompt]
        )
        return response.text.strip()
    except Exception as e:
        raise LLMServiceError(f"Failed to grade essay: {str(e)}")

def grade_mcqs(generated: str, user_answer: str) -> str:
    template = _load_prompt("grade_mcq.txt")
    grading_prompt = template.format(generated=generated, user_answer=user_answer)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[grading_prompt]
        )
        return response.text.strip()
    except Exception as e:
        raise LLMServiceError(f"Failed to grade MCQs: {str(e)}")

def tutoring_chat(text: str, history: list[str], question: str) -> str:
    template = _load_prompt("tutoring_chat.txt")
    history_str = "\n".join(history) if history else "No previous conversation"
    chat_prompt = template.format(text=text, history=history_str, question=question)
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[chat_prompt]
        )
        return response.text.strip()
    except Exception as e:
        raise LLMServiceError(f"Failed to process chat: {str(e)}") 