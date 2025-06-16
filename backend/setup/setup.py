
import anyio
import os

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from contextlib import asynccontextmanager
from asyncio import Event

from ..sqlm.sqlm_tables import Base  


DATABASE_URL = os.environ.get('DATABASE_URL')

# -------------- setup --------------
async def set_threadpool_tokens(number_of_tokens: int = 100) -> None:
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = number_of_tokens


@asynccontextmanager
async def lifespan(app: FastAPI):

    initialization_complete = Event()
    app.state.initialization_complete = initialization_complete

    # 🔧 Set up DB engine and session
    engine = create_async_engine(DATABASE_URL, echo=False, future=True)
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    app.state.engine = engine
    app.state.sessionmaker = SessionLocal

    print("app.state:", app.state.sessionmaker)

    await set_threadpool_tokens()

    try:

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        initialization_complete.set()
        yield

    finally:
        await engine.dispose()
        print("DB engine disposed")

# -------------- application --------------
def create_application(router: APIRouter) -> FastAPI:
    """Creates and configures a FastAPI application based on the provided settings.
    """

    application = FastAPI(lifespan=lifespan)
    application.include_router(router)

    origins = [
    "http://localhost:3000", 
    "http://localhost:5050",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"], 
        allow_headers=["*"],
    )

    def show_routes():
        for route in application.router.routes:
            print(f"{route.path} → {route.name} ({route.methods})")

    show_routes()

    return application
