import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from nubit import bot
from nubit.api import auth, weeks, entries, votes

BOT_TOKEN = os.environ["BOT_TOKEN"]


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.start(BOT_TOKEN))

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(weeks.router, prefix="/auth")
api_router.include_router(entries.router, prefix="/auth")
api_router.include_router(votes.router, prefix="/auth")

app.include_router(api_router, prefix="/api")
