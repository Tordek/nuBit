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

@router.post("/discord")
async def oauth(request: OauthRequest, response: Response) -> SessionData:
    scope = ["identify", "guilds"]
    discord = OAuth2Session(client_id=CLIENT_ID, scope=scope,
                            redirect_uri="http://localhost:8080/oauth/discord/")

    try:
        discord.fetch_token(
            token_url="https://discord.com/api/oauth2/token",
            client_secret=CLIENT_SECRET,
            code=request.authorization_response
        )
    except OAuth2Error:
        raise HTTPException(status_code=401, detail="Failure obtaining data")

    # Fetch user's nickname
    user_request = discord.get("https://discord.com/api/users/@me")
    if 200 > user_request.status_code or user_request.status_code > 299:
        raise HTTPException(
            status_code=401, detail="Failure obtaining user data")
    user_data = user_request.json()

    # Check if user is in 8BMT's server
    channels_request = discord.get("https://discord.com/api/users/@me/guilds")
    if 200 > channels_request.status_code or user_request.status_code > 299:
        raise HTTPException(
            status_code=401, detail="Failure obtaining guild data")
    servers_data = channels_request.json()

    if not any(True for server in servers_data if server["id"] == SERVER_ID):
        raise HTTPException(status_code=401, detail="User is not in 8BMT")

    user = SessionData(
        user_id=user_data["id"],
        username=user_data["username"],
        avatar=user_data["avatar"],
        is_admin=False
    )
    await session.create_session(user, response)

    return user


@router.get("/me")
async def me(session_info: Optional[SessionInfo] = Depends(session)) -> SessionData:
    if session_info is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return session_info[1]
