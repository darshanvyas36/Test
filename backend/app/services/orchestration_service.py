from . import account_service, ai_service, instagram_service
import asyncio
import os

async def run_full_pipeline(account_id: str, simple_prompt: str, hashtags: str):
    """
    Runs the entire content creation and posting pipeline for a single account.
    """
    print(f"--- Starting full pipeline for account {account_id} ---")
    video_path = None
    try:
        account = await account_service.get_account_by_id(account_id)
        if not account:
            raise ValueError(f"Account {account_id} not found.")

        print("Step 1: Elaborating prompt...")
        elaborated_prompt = ai_service.elaborate_prompt(simple_prompt)

        print("Step 2: Generating video...")
        video_path = ai_service.generate_video(elaborated_prompt)
        if not video_path:
            raise ValueError("Video generation failed.")

        print("Step 3: Uploading to Instagram...")
        caption = f"{simple_prompt}\n.\n.\n.\n{hashtags}"
        client = instagram_service.get_instagram_client(account)
        media = instagram_service.upload_reel(client, video_path, caption)

        return {"status": "success", "media_id": media.id, "account_id": account_id}
    except Exception as e:
        return {"status": "error", "message": str(e), "account_id": account_id}
    finally:
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
            print(f"Cleaned up video file: {video_path}")

async def run_pipeline_for_all_accounts(simple_prompt: str, hashtags: str):
    """
    Runs the full pipeline for all managed accounts concurrently.
    """
    all_accounts = await account_service.get_all_accounts()
    if not all_accounts:
        return []

    tasks = [run_full_pipeline(str(account.id), simple_prompt, hashtags) for account in all_accounts]
    return await asyncio.gather(*tasks)
