import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from app.database import init_db
from app.routes import journals, stories, stats

app = FastAPI(title="StoryVault API")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
origins = list({FRONTEND_URL, "http://localhost:5173"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "StoryVault API is running"}


app.include_router(journals.router, prefix="/api/journals")
app.include_router(stories.router, prefix="/api/stories")
app.include_router(stats.router, prefix="/api/stats")


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
