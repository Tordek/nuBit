from nubit import compo
from nubit.helpers import require_login, session
import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import OAuth2Error

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
SERVER_ID = os.environ["SERVER_ID"]


class OauthRequest(BaseModel):
    authorization_response: str


router = APIRouter()


@router.get("/me", dependencies=[Depends(require_login)])
def view_my_submission(session_info=Depends(session)):
    week = compo.get_week(True)
    votes = week['votes']
    for vote in votes:
        if vote['userID'] == session_info["user_id"]:
            return vote

    return {}


@router.put("/me", dependencies=[Depends(require_login)])
def update_my_submission(session_info=Depends(session)):
    week = compo.get_week(True)
    week['votes'] = [
        vote
        for vote in week['votes']
        if vote['userID'] != session_info["user_id"]
    ]
    return {}
