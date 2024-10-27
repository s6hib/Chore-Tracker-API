from fastapi import APIRouter, Depends
from src.api import auth

router = APIRouter(
    prefix="/chore",
    tags=["chore"],
    dependencies=[Depends(auth.get_api_key)],
)


