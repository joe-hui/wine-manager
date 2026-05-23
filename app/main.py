from fastapi import FastAPI

from app.health import router as health_router
from app.routes import router as winery_router, wine_router, note_router


def create_app() -> FastAPI:
    app = FastAPI(title="Wine Manager", version="1.0.0")

    app.include_router(health_router)
    app.include_router(winery_router)
    app.include_router(wine_router)
    app.include_router(note_router)

    return app


app = create_app()
