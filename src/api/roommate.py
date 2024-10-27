from fastapi import APIRouter, Depends
from src.api import auth

router = APIRouter(
    prefix="/roommate",
    tags=["roommate"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/roommates/", tags=["roommate"])
def get_roommates():
    
    return "test"
