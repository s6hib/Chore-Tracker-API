from fastapi import APIRouter, Depends
from src.api import auth

router = APIRouter(
    prefix="/roommate",
    tags=["roommate"],
    dependencies=[Depends(auth.get_api_key)],
)
