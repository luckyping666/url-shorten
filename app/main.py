from fastapi import FastAPI
from api.routes.shortener import router as shortener_router
from api.routes.stats import router as stats_router

app = FastAPI(title="URL Shortener")

app.include_router(shortener_router)
app.include_router(stats_router)
