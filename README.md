# AI-Powered Instagram Automation and Management Dashboard

This project is a full-stack web application designed to manage and automate content creation for multiple Instagram accounts. It features a Python (FastAPI) backend with an AI pipeline for generating video content and a simple, lightweight vanilla JavaScript frontend for user interaction. The entire application is containerized with Docker and orchestrated with Docker Compose for easy setup and deployment.

## Features

- **Account Management:** Add and delete Instagram accounts securely. Passwords are encrypted in the database.
- **AI Content Pipeline:**
    1.  Provide a simple text prompt (e.g., "a cat playing in the sun").
    2.  An AI model elaborates this into a detailed, cinematic prompt.
    3.  A second AI model generates a short video based on the detailed prompt.
- **Automated Posting:** The generated video is automatically uploaded to Instagram as a Reel with user-provided hashtags.
- **Post to All:** A single click can trigger the content creation pipeline for all managed accounts simultaneously.
- **Post to Single Account:** Option to generate content and post to a specific account.
- **Dockerized:** The entire application stack can be run with a single `docker-compose` command.

## How to Run the Project

### Prerequisites

- Docker
- Docker Compose

### Step 1: Create the Environment File

Before you can run the application, you need to provide your secret keys and credentials. Create a file named `.env` in the root of the project directory.

Copy the following content into the `.env` file and replace the placeholder values with your actual credentials:

```
# .env

# --- MongoDB Settings ---
# Replace with your MongoDB Atlas connection string
MONGO_CONNECTION_STRING="mongodb+srv://<user>:<password>@<cluster-url>/<db-name>?retryWrites=true&w=majority"

# --- Security Settings ---
# Replace with a long, random string for encrypting passwords (e.g., generated with `openssl rand -hex 32`)
SECRET_KEY="your_super_secret_key_for_encryption"

# --- AI Services Settings ---
# Replace with your Hugging Face API token (get one from https://huggingface.co/settings/tokens)
HUGGING_FACE_API_TOKEN="hf_YourHuggingFaceToken"
```

### Step 2: Build and Run with Docker Compose

Open your terminal in the project root directory and run the following command:

```bash
docker-compose up --build
```

This command will:
- Build the backend Docker image.
- Pull the nginx image for the frontend.
- Start both containers and connect them.

The first time you run this, it may take several minutes to download the base images and install all the dependencies.

### Step 3: Access the Application

Once the services are running, you can access the web dashboard in your browser at:

**http://localhost:8080**

### Managing the Application

- To stop the application, press `Ctrl+C` in the terminal where `docker-compose` is running.
- To stop and remove the containers, run: `docker-compose down`
- To run in the background (detached mode), use: `docker-compose up --build -d`
- To view the logs from the running services, use: `docker-compose logs -f`
