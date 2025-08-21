import os
from typing import Final

# --- Environment Variables ---
# It is highly recommended to use a .env file to manage your environment variables.
# Create a file named `.env` in the `backend/` directory and add the following variables.
# Example:
# MONGO_CONNECTION_STRING="mongodb+srv://<user>:<password>@<cluster-url>/<db-name>?retryWrites=true&w=majority"
# SECRET_KEY="your_super_secret_key_for_encryption"
# HUGGING_FACE_API_TOKEN="your_hugging_face_api_token"

# --- MongoDB Settings ---
MONGO_CONNECTION_STRING: Final[str] = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017/")
DATABASE_NAME: Final[str] = "instagram_automation_db"

# --- Security Settings ---
SECRET_KEY: Final[str] = os.getenv("SECRET_KEY", "a_default_secret_key_that_must_be_changed_in_production")
ENCRYPTION_ALGORITHM: Final[str] = "Fernet"

# --- AI Services Settings ---
HUGGING_FACE_API_TOKEN: Final[str] = os.getenv("HUGGING_FACE_API_TOKEN")
TEXT_GENERATION_MODEL_ID: Final[str] = "mistralai/Mistral-7B-Instruct-v0.2"
VIDEO_GENERATION_MODEL_ID: Final[str] = "cerspense/zeroscope_v2_576w"

# --- File Storage Settings ---
GENERATED_CONTENT_DIR: Final[str] = "backend/generated_content"
INSTAGRAM_SESSION_DIR: Final[str] = "backend/instagram_sessions"
