from nubit.bot import is_admin
import os
from fastapi_sessions import SessionCookie
from fastapi_sessions.backends import InMemoryBackend
from pydantic.main import BaseModel

COOKIE_SECRET = os.environ["COOKIE_SECRET"]


class SessionData(BaseModel):
    user_id: str
    username: str
    avatar: str
    is_admin: bool


backend = InMemoryBackend()
session = SessionCookie(
    name="session",
    secret_key=COOKIE_SECRET,
    data_model=SessionData,
    backend=backend,
    auto_error=False
)
