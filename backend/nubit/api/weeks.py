import os
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from nubit.helpers import require_admin, require_login, session
from nubit import compo

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
SERVER_ID = os.environ["SERVER_ID"]


class OauthRequest(BaseModel):
    authorization_response: str


router = APIRouter()


@router.get("/current")
def get_current_week():
    return format_week(compo.get_week(True))


@router.put("/current", dependencies=[Depends(require_admin)])
def update_current_week():
    week = compo.get_week(True)


@router.get("/next")
def get_current_week():
    return format_week(compo.get_week(False))


@router.put("/next", dependencies=[Depends(require_admin)])
def update_current_week():
    week = compo.get_week(False)


# Helpers
def format_week(week: dict, is_admin: bool) -> dict:
    """
    Massages week data into the format that will be output as JSON.
    """
    entryData = []

    for e in week["entries"]:
        is_valid = compo.entry_valid(e)
        if not is_admin and not is_valid:
            continue

        prunedEntry = {
            "uuid": e["uuid"],
            "pdfUrl": f"/files/{e['uuid']}/{e.get('pdfFilename')}",
            "mp3Format": e.get("mp3Format"),
            "entryName": e["entryName"],
            "entrantName": e["entrantName"],
            "isValid": is_valid,
        }

        if is_admin and "entryNotes" in e:
            prunedEntry["entryNotes"] = e["entryNotes"]

        if e.get("mp3Format") == "mp3":
            prunedEntry["mp3Url"] = f"/files/{e['uuid']}/{e['mp3Filename']}"
        else:
            prunedEntry["mp3Url"] = e.get("mp3")

        entryData.append(prunedEntry)

    return {
        "entries": entryData,
        "theme": week["theme"],
        "date": week["date"],
        "submissionsOpen": week["submissionsOpen"],
        "votingOpen": week["votingOpen"],
        "voteParams": week["voteParams"],
    }
