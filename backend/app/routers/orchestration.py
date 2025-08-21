from fastapi import APIRouter, HTTPException, status, Body
from pydantic import BaseModel, Field
from ..services import orchestration_service

router = APIRouter()

class PipelineRequest(BaseModel):
    simple_prompt: str = Field(..., description="The simple prompt to generate content from.")
    hashtags: str = Field(..., description="The hashtags to include in the caption.")

class SinglePipelineRequest(PipelineRequest):
    account_id: str = Field(..., description="The ID of the account to run the pipeline for.")

@router.post(
    "/run-for-account",
    summary="Run the full pipeline for a single account",
)
async def run_pipeline_for_single_account(request: SinglePipelineRequest = Body(...)):
    result = await orchestration_service.run_full_pipeline(
        account_id=request.account_id,
        simple_prompt=request.simple_prompt,
        hashtags=request.hashtags
    )
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@router.post(
    "/run-for-all",
    summary="Run the full pipeline for all managed accounts",
)
async def run_pipeline_for_all_accounts(request: PipelineRequest = Body(...)):
    results = await orchestration_service.run_pipeline_for_all_accounts(
        simple_prompt=request.simple_prompt,
        hashtags=request.hashtags
    )
    return results
