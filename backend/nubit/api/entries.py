from fastapi import APIRouter, HTTPException, Depends
from nubit import bot
from nubit import compo
from nubit.helpers import require_login, session


router = APIRouter()


@router.get("/me", dependencies=[Depends(require_login)])
def view_my_submission(session_info=Depends(session)):
    week = compo.get_week(True)
    if not week["submissionsOpen"]:
        raise HTTPException(
            status_code=401, detail="Submissions are currently closed")

    entry = get_editable_entry(
        compo.find_entry_by_user(week, session_info["user_id"]))

    return entry


@router.delete("/me", dependencies=[Depends(require_login)])
def delete_my_submission(session_info=Depends(session)):
    pass


@router.put("/me", dependencies=[Depends(require_login)])
def delete_my_submission(session_info=Depends(session)):
    bot.entry_info_message({})
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
        entry_data["mp3Url"] = f"/files/{entry['uuid']}/{entry['mp3Filename']}"
    else:
        entry_data["mp3Url"] = entry.get("mp3")

    if entry.get("pdfFilename") is not None:
        entry_data["pdfUrl"] = f"/files/{entry['uuid']}/{entry.get('pdfFilename')}"

    return entry_data
