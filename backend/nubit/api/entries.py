from typing import Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File, Form
from nubit import bot
from nubit import compo
from nubit.helpers import require_login, session


router = APIRouter()


@router.get("/me/next", dependencies=[Depends(require_login)])
def view_my_submission(session_info=Depends(session)):
    week = compo.get_week(False)
    entry = compo.find_entry_by_user(week, session_info["user_id"])

    if entry is None:
        raise HTTPException(
            status_code=404, detail="You didn't submit anything")

    return get_entry_results(entry)


@router.get("/me/next", dependencies=[Depends(require_login)])
def view_my_submission(session_info=Depends(session)):
    week = compo.get_week(True)
    entry = compo.find_entry_by_user(week, session_info["user_id"])

    if entry is None:
        raise HTTPException(
            status_code=404, detail="You haven't submitted anything")

    return get_editable_entry(entry)


@router.delete("/me/next", dependencies=[Depends(require_login)])
def delete_my_submission(session_info=Depends(session)):
    raise NotImplementedError()
    week = compo.get_week(True)
    if not week["submissionsOpen"]:
        raise HTTPException(
            status_code=401, detail="Submissions are currently closed")

    entry = compo.find_entry_by_user(week, session_info["user_id"])

    if entry is None:
        raise HTTPException(
            status_code=404, detail="You haven't submitted anything")

    pass


@router.put("/me/next", dependencies=[Depends(require_login)])
async def update_my_submission(
    session_info=Depends(session),
    name: str = Form(...),
    pdfFile: Optional[UploadFile] = File(None),
    mp3File: Optional[UploadFile] = File(None),
    mp3Link: Optional[str] = Form(None),
):
    week = compo.get_week(True)
    if not week["submissionsOpen"]:
        raise HTTPException(
            status_code=401, detail="Submissions are currently closed")

    entry = compo.find_entry_by_user(week, session_info["user_id"])

    if entry is None:
        entry = compo.create_blank_entry(
            session_info["username"],
            session_info["user_id"]
        )
        week["entries"].append(entry)

    entry["entryName"] = name
    if pdfFile is not None:
        entry["pdfFormat"] = "pdf"
        entry["pdfFilename"] = pdfFile.filename
        entry["pdf"] = await pdfFile.read()

    if mp3File is not None:
        entry["mp3Format"] = "mp3"
        entry["mp3Filename"] = mp3File.filename
        entry["mp3"] = await mp3File.read()

    if mp3Link is not None:
        entry["mp3Format"] = "external"
        entry["mp3Filename"] = None
        entry["mp3"] = mp3Link

    bot.entry_info_message(entry)
    return get_editable_entry(entry)


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
        entry_data["mp3Url"] = f"/files/{entry['uuid']}/{entry['mp3Filename']}"
    else:
        entry_data["mp3Url"] = entry.get("mp3")

    if entry.get("pdfFilename") is not None:
        entry_data["pdfUrl"] = f"/files/{entry['uuid']}/{entry.get('pdfFilename')}"

    return entry_data


def get_entry_results(week: dict, entry: dict) -> dict:
    pass
