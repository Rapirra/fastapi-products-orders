from fastapi import FastAPI

from app.config.database.database import Base, engine
from app.modules import router as api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)


