from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..services import llm_service
from ..services.llm_service import LLMServiceError

router = APIRouter()

class ChatRequest(BaseModel):
    text: str
    history: Optional[List[str]] = None
    question: str

class ChatResponse(BaseModel):
    result: str

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Educational content is required")
    history = req.history if req.history else []
    
    try:
        result = llm_service.tutoring_chat(req.text, history, req.question.strip())
        return ChatResponse(result=result)
    except LLMServiceError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 