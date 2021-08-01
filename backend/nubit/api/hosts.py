import os
from fastapi import APIRouter

VALID_HOSTS = os.environ["VALID_HOSTS"]


router = APIRouter()
@router.get("/")
def get_valid_hosts():
    return VALID_HOSTS.split()