from fastapi import APIRouter, HTTPException, status, Body
from pydantic import BaseModel, Field
from ..services.ai_service import elaborate_prompt, generate_video

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=100)

class PromptResponse(BaseModel):
    original_prompt: str
    elaborated_prompt: str

class VideoGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=500)

class VideoGenerationResponse(BaseModel):
    prompt: str
    video_path: str

@router.post(
    "/elaborate",
    response_model=PromptResponse,
    summary="Elaborate a simple prompt using an LLM"
)
async def elaborate_user_prompt(request: PromptRequest = Body(...)):
    try:
        elaborated = elaborate_prompt(request.prompt)
        return PromptResponse(original_prompt=request.prompt, elaborated_prompt=elaborated)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post(
    "/generate-video",
    response_model=VideoGenerationResponse,
    summary="Generate a video from a detailed prompt"
)
async def generate_video_from_prompt(request: VideoGenerationRequest = Body(...)):
    try:
        video_path = generate_video(request.prompt)
        if not video_path:
            raise HTTPException(status_code=500, detail="Video generation failed.")
        return VideoGenerationResponse(prompt=request.prompt, video_path=video_path)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
