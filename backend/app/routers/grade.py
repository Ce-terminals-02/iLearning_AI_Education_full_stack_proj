from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services import llm_service
from ..services.llm_service import LLMServiceError

router = APIRouter()

class GradeRequest(BaseModel):
    text: str
    mode: str
    user_answer: str
    generated: str

class GradeResponse(BaseModel):
    result: str

@router.post("/grade", response_model=GradeResponse)
def grade(req: GradeRequest) -> GradeResponse:
    if req.mode not in {"essay", "mcq"}:
        raise HTTPException(status_code=400, detail="Invalid mode. Supported values are 'essay' or 'mcq'.")

    try:
        if req.mode == "essay":
            result = llm_service.grade_essay(req.text, req.generated, req.user_answer)
        else:
            result = llm_service.grade_mcqs(req.generated, req.user_answer)

        return GradeResponse(result=result)
    except LLMServiceError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")