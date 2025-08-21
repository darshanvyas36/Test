import requests
from ..core.config import (
    HUGGING_FACE_API_TOKEN,
    TEXT_GENERATION_MODEL_ID,
    VIDEO_GENERATION_MODEL_ID,
    GENERATED_CONTENT_DIR
)
import json
import time
import uuid
import os
import pathlib

TEXT_GEN_API_URL = f"https://api-inference.huggingface.co/models/{TEXT_GENERATION_MODEL_ID}"
VIDEO_GEN_API_URL = f"https://api-inference.huggingface.co/models/{VIDEO_GENERATION_MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"}

def elaborate_prompt(simple_prompt: str) -> str:
    """
    Calls the Hugging Face Inference API to elaborate on a simple prompt.
    """
    if not HUGGING_FACE_API_TOKEN:
        print("WARNING: HUGGING_FACE_API_TOKEN is not set. Skipping prompt elaboration.")
        return simple_prompt

    instructional_prompt = (
        f"Based on the following idea, create a highly detailed, creative, and cinematic "
        f"prompt for an AI video generator. The prompt should be a single, descriptive paragraph. "
        f"Focus on visual details, lighting, camera angles, and atmosphere.\n\n"
        f"Idea: '{simple_prompt}'\n\n"
        f"Detailed Video Prompt:"
    )
    payload = {"inputs": instructional_prompt, "parameters": {"max_new_tokens": 150, "temperature": 0.8, "top_p": 0.9, "do_sample": True, "return_full_text": False}}
    try:
        response = requests.post(TEXT_GEN_API_URL, headers=HEADERS, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()
        if result and isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text'].strip()
    except Exception as e:
        print(f"An error occurred during prompt elaboration: {e}")
    return simple_prompt

def generate_video(prompt: str) -> str:
    """
    Calls the Hugging Face Inference API to generate a video from a prompt.
    """
    if not HUGGING_FACE_API_TOKEN:
        print("WARNING: HUGGING_FACE_API_TOKEN is not set. Skipping video generation.")
        return None

    payload = {"inputs": prompt}
    try:
        response = requests.post(VIDEO_GEN_API_URL, headers=HEADERS, json=payload, timeout=20)
        if response.headers.get("content-type") == "video/mp4":
            return _save_video_content(response.content)

        response.raise_for_status()
        result = response.json()

        if 'estimated_time' in result and 'scheduler' in result:
            polling_url = f"{VIDEO_GEN_API_URL}/queue/fetch/{result['id']}"
            for _ in range(20):
                time.sleep(10)
                poll_response = requests.get(polling_url, headers=HEADERS)
                poll_result = poll_response.json()
                if poll_result['status'] == 'completed':
                    video_url = poll_result['output'][0]
                    video_response = requests.get(video_url)
                    video_response.raise_for_status()
                    return _save_video_content(video_response.content)
                elif poll_result['status'] in ['failed', 'error']:
                    print(f"Video generation failed. Reason: {poll_result.get('reason')}")
                    return None
            print("Polling timed out.")
            return None
    except Exception as e:
        print(f"An error occurred during video generation: {e}")
    return None

def _save_video_content(content: bytes) -> str:
    """Saves video content to a file and returns the path."""
    pathlib.Path(GENERATED_CONTENT_DIR).mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(GENERATED_CONTENT_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(content)
    print(f"Video saved to {filepath}")
    return filepath
