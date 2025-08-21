from fastapi import APIRouter, HTTPException, status, Body
from pydantic import BaseModel, Field
from ..services import instagram_service, account_service

router = APIRouter()

class ReelUploadRequest(BaseModel):
    account_id: str = Field(..., description="The ID of the account to post from.")
    video_path: str = Field(..., description="The local server path to the generated video file.")
    caption: str = Field(..., max_length=2200, description="The caption for the Reel.")

class ReelUploadResponse(BaseModel):
    media_id: str
    media_url: str

@router.post(
    "/upload-reel",
    response_model=ReelUploadResponse,
    summary="Upload a video as an Instagram Reel"
)
async def upload_instagram_reel(request: ReelUploadRequest = Body(...)):
    """
    Endpoint to upload a video to Instagram as a Reel.
    """
    account = await account_service.get_account_by_id(request.account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")

    try:
        client = instagram_service.get_instagram_client(account)
        media = instagram_service.upload_reel(client, request.video_path, request.caption)
        if not media:
            raise HTTPException(status_code=500, detail="Failed to upload Reel.")

        return ReelUploadResponse(
            media_id=media.id,
            media_url=f"https://www.instagram.com/p/{media.code}/"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
