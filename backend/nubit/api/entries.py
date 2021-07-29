import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi_sessions.session_cookie import SessionInfo
from pydantic import BaseModel
from nubit.bot import Bot
from nubit.api.session import SessionData, session


class OauthRequest(BaseModel):
    authorization_response: str


router = APIRouter()


@router.get("/")
def list_entries(session_info: Optional[SessionInfo] = Depends(session)):
    if session_info is not None:
        # fetch votes
        pass

    if not session_info[1].is_admin:
        # remove gossip
        pass

    pass


@router.post("/")
def submit(session_info: Optional[SessionInfo] = Depends(session)):
    pass


@router.get("/me")
def view_my_submission(session_info: Optional[SessionInfo] = Depends(session)):
    if session_info is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not session_info[1].is_admin:
        # remove gossip
        pass
    
    pass


@router.delete("/me")
def delete_my_submission(session_info: Optional[SessionInfo] = Depends(session)):
    if session_info is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    pass
