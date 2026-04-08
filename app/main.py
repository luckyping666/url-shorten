from fastapi import FastAPI
from app.api.routes.shortener import router as shortener_router
from app.api.routes.stats import router as stats_router
from app.core.database import engine, Base

app = FastAPI(title="URL Shortener")


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(shortener_router)
app.include_router(stats_router)
