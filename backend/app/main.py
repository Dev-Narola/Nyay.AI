from fastapi import FastAPI
from app.core.config import get_settings
from app.api import api_router

def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Nyay.AI Backend",
        debug=settings.DEBUG
    )

    app.include_router(api_router)

    return app

app = create_app()

@app.get("/")
async def root():
    return {"message": "Hello World"}
