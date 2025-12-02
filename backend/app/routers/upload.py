from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from ..services import file_service

router = APIRouter()

class UploadResponse(BaseModel):
    text: str

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    try:
        content = await file.read()
        text = file_service.extract_text(file.filename, content)
        return UploadResponse(text=text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 