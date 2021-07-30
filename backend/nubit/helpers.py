from fastapi import Request, HTTPException


async def require_login(request: Request):
    if "username" not in request.session:
        raise HTTPException(status_code=401, detail="Unauthorized")


async def require_admin(request: Request):
    await require_login(request)

    if not request.session["is_admin"]:
        raise HTTPException(status_code=401, detail="Unauthorized")


async def session(request: Request):
    return request.session
