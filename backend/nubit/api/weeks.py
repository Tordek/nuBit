import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi_sessions.session_cookie import SessionInfo
from pydantic import BaseModel
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from nubit.api.session import SessionData, session

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
SERVER_ID = os.environ["SERVER_ID"]


class OauthRequest(BaseModel):
    authorization_response: str

router = APIRouter()