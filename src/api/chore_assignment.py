from fastapi import APIRouter, Depends
from src.api import auth

router = APIRouter(
    prefix="/chore_assignment",
    tags=["chore_assignment"],
    dependencies=[Depends(auth.get_api_key)],
)
