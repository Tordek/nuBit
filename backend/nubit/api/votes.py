from fastapi.param_functions import Body
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
def get_votes(session_info=Depends(session)):
    votes = compo.get_week(False)['votes']
    for vote in votes:
        if vote['userID'] == session_info["user_id"]:
            return vote['ratings']

    return []


@router.put("/me", dependencies=[Depends(require_login)])
def vote(body = Body(...), session_info=Depends(session)):
    votes = body["votes"]
    week = compo.get_week(False)
    week['votes'] = [
        vote
        for vote in week['votes']
        if vote['userID'] != session_info["user_id"]
    ]

    user_entry = compo.find_entry_by_user(week, session_info["user_id"])

    if user_entry is not None:
        votes = [vote for vote in votes if vote["entryUUID"] != user_entry["uuid"]]

        max_vote = max(vote["rating"] for vote in votes)

        for param in week["voteParams"]:
            votes.append({
                "entryUUID": user_entry["uuid"],
                "voteForName": user_entry["userName"],
                "voteParam": param["name"],
                "rating": max_vote                
            })

    ratings = [
        {
            "entryUUID": vote["entryUUID"],
            "voteForName": vote["voteForName"],
            "voteParam": vote["voteParam"],
            "rating": vote["rating"]
        }
        for vote in votes
    ]

    week['votes'].append({
        "userID": session_info["user_id"],
        "userName": session_info["username"],
        "ratings": ratings
    })

    return {}
