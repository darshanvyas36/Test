from instagrapi import Client
from instagrapi.types import Media
from ..core.config import INSTAGRAM_SESSION_DIR
from ..core.security import decrypt_password
from ..models.account import AccountInDB
import os
import pathlib

def get_instagram_client(account: AccountInDB) -> Client:
    """
    Initializes and returns an authenticated instagrapi client.
    """
    cl = Client()
    pathlib.Path(INSTAGRAM_SESSION_DIR).mkdir(parents=True, exist_ok=True)
    session_file = os.path.join(INSTAGRAM_SESSION_DIR, f"{account.username}.json")

    try:
        if os.path.exists(session_file):
            cl.load_settings(session_file)
        cl.login(account.username, decrypt_password(account.hashed_password))
        cl.dump_settings(session_file)
    except Exception as e:
        print(f"Failed to login to Instagram for user {account.username}: {e}")
        raise

    return cl

def upload_reel(client: Client, video_path: str, caption: str) -> Media:
    """
    Uploads a video file to Instagram as a Reel.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found at path: {video_path}")

    try:
        media = client.clip_upload(
            path=pathlib.Path(video_path),
            caption=caption,
        )
        return media
    except Exception as e:
        print(f"Failed to upload Reel for user {client.username}: {e}")
        raise
