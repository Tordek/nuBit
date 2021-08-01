import os
from typing import Optional
import discord
from fastapi import APIRouter, HTTPException, Depends, Response, Request
from pydantic import BaseModel
from requests import sessions
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import OAuth2Error
from nubit import bot
from nubit.helpers import require_login, session

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
SERVER_ID = os.environ["SERVER_ID"]
ADMIN_ROLE_ID = os.environ["ADMIN_ROLE_ID"]
DISCORD_SCOPES = ["identify"]


class OauthRequest(BaseModel):
    code: str
    state: str
    redirectUri: str


router = APIRouter()


@router.get("/discord")
async def get_login_url(redirectUri: str, session=Depends(session)):

    discord_client = OAuth2Session(client_id=CLIENT_ID,
                                   scope=DISCORD_SCOPES,
                                   redirect_uri=redirectUri)

    authorization_url, state = discord_client.authorization_url(
        'https://discord.com/api/oauth2/authorize')

    session['state'] = state
    return {"authUrl": authorization_url}


@router.post("/discord")
async def oauth(oauth: OauthRequest, session=Depends(session)):
    discord_client = OAuth2Session(client_id=CLIENT_ID,
                                   scope=DISCORD_SCOPES,
                                   state=session['state'],
                                   redirect_uri=oauth.redirectUri)
    # Verify the token
    try:
        token = discord_client.fetch_token(
            token_url="https://discord.com/api/oauth2/token",
            client_secret=CLIENT_SECRET,
            code=oauth.code,
            state=oauth.state
        )
    except OAuth2Error:
        raise HTTPException(status_code=401, detail="Failure obtaining data")

    # Fetch user's nickname
    user_request = discord_client.get("https://discord.com/api/users/@me")
    if 200 > user_request.status_code or user_request.status_code > 299:
        raise HTTPException(
            status_code=401, detail="Failure obtaining user data")
    user_data = user_request.json()

    # Validate if user is admin
    guild = bot.client.get_guild(int(SERVER_ID))
    try:
        member = await guild.fetch_member(user_data["id"])
    except discord.errors.NotFound:
        raise HTTPException(
            status_code=401, detail="User is not a member of the server")

    is_admin = int(ADMIN_ROLE_ID) in member.roles
    avatar = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.png"

    del session['state']
    session['user_id'] = user_data["id"]
    session['username'] = member.nick or user_data["username"]
    session['avatar'] = avatar
    session['is_admin'] = is_admin
    session['access_token'] = token["access_token"]
    session['refresh_token'] = token["refresh_token"]

    return {
        'user_id': session['user_id'],
        'username': session['username'],
        'avatar': session['avatar'],
        'is_admin': session['is_admin'],
    }


@router.get("/me", dependencies=[Depends(require_login)])
async def me(session=Depends(session)):
    return {
        'user_id': session['user_id'],
        'username': session['username'],
        'avatar': session['avatar'],
        'is_admin': session['is_admin'],
    }


@router.post("/logout", dependencies=[Depends(require_login)])
async def logout(session=Depends(session)):
    session.clear()
    return {}
