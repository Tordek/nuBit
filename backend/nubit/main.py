import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import asyncio
from nubit import bot
from nubit.api import auth, weeks, entries, votes, hosts

BOT_TOKEN = os.environ["BOT_TOKEN"]


COOKIE_SECRET = os.environ["COOKIE_SECRET"]
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

app.add_middleware(
    SessionMiddleware,
    secret_key=COOKIE_SECRET
)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.client.start(BOT_TOKEN))

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(weeks.router, prefix="/weeks")
api_router.include_router(entries.router, prefix="/entries")
api_router.include_router(votes.router, prefix="/votes")
api_router.include_router(hosts.router, prefix="/hosts")

app.include_router(api_router, prefix="/api")
