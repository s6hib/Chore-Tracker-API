from fastapi import APIRouter, Depends
from src.api import auth

router = APIRouter(
    prefix="/roommate_list",
    tags=["roommate_list"],
    dependencies=[Depends(auth.get_api_key)],
)
