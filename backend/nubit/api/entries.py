import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi_sessions.session_cookie import SessionInfo
from pydantic import BaseModel
from nubit import bot
from nubit.api.session import SessionData, session
from nubit import compo


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
    if session_info is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    pass


@router.get("/me")
def view_my_submission(session_info: Optional[SessionInfo] = Depends(session)):
    if session_info is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not compo.get_week(True)["submissionsOpen"]:
        raise HTTPException(
            status_code=401, detail="Submissions are currently closed")

    entry = compo.find_entry_by_user(session_info[1])

    if not session_info[1].is_admin:
        # remove gossip
        pass

    return get_editable_entry(entry)


@router.delete("/me")
def delete_my_submission(session_info: Optional[SessionInfo] = Depends(session)):
    if session_info is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    pass


# Helpers
def get_editable_entry(entry: dict) -> dict:
    entry_data = {
        "uuid": entry["uuid"],
        "entryName": entry["entryName"],
        "entrantName": entry["entrantName"],
        "pdfUrl": None,
        "mp3Format": entry.get("mp3Format"),
    }

    if entry.get("mp3Format") == "mp3":
        entry_data["mp3Url"] = "/files/%s/%s" % (
            entry["uuid"], entry["mp3Filename"])
    else:
        entry_data["mp3Url"] = entry.get("mp3")

    if entry.get("pdfFilename") is not None:
        entry_data["pdfUrl"] = "/files/%s/%s" % (
            entry["uuid"], entry.get("pdfFilename"))

    return entry_data
