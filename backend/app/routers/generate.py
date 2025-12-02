from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services import llm_service
from ..services.llm_service import LLMServiceError

router = APIRouter()

class GenerateRequest(BaseModel):
    text: str
    mode: str

class GenerateResponse(BaseModel):
    result: str

@router.post("/generate", response_model=GenerateResponse)
def generate_content(req: GenerateRequest) -> GenerateResponse:
    if req.mode not in {"essay", "mcq"}:
        raise HTTPException(status_code=400, detail="Invalid mode. Supported values are 'essay' or 'mcq'.")

    try:
        if req.mode == "essay":
            result = llm_service.generate_essay_prompt(req.text)
        else:
            result = llm_service.generate_mcqs(req.text)

        return GenerateResponse(result=result)
    except LLMServiceError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")