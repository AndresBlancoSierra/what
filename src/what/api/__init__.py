from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from what.database.engine import init_db, dispose_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await dispose_db()


def create_app() -> FastAPI:
    app = FastAPI(title="WHAT?", version="0.1.0", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    from what.api.routes import router
    app.include_router(router, prefix="/api")
    return app


def serve(host: str = "127.0.0.1", port: int = 8001) -> None:
    import uvicorn
    app = create_app()
    uvicorn.run(app, host=host, port=port, log_level="info")


app = create_app()
