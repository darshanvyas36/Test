from fastapi import FastAPI
from .db import connect_to_mongo, close_mongo_connection
from .routers import accounts, ai, instagram, orchestration

app = FastAPI(
    title="AI-Powered Instagram Automation and Management Dashboard",
    description="A web dashboard to manage and automate Instagram content creation using AI.",
    version="0.1.0"
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    close_mongo_connection()

# Include the API routers
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(ai.router, prefix="/ai", tags=["AI Services"])
app.include_router(instagram.router, prefix="/instagram", tags=["Instagram"])
app.include_router(orchestration.router, prefix="/orchestration", tags=["Orchestration"])

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the AI-Powered Instagram Automation API"}
