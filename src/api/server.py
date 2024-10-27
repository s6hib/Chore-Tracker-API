from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import chore, roommate, chore_assignment
import json
import logging
from starlette.middleware.cors import CORSMiddleware

description = """
Chore Tracker API helps roommates manage and track household chores.
"""

app = FastAPI(
    title="Chore Tracker API",
    description=description,
    version="1.0.0",
    contact={
        "name": "Chore Tracker LLC. Inc. Co. Est.1987",
        "email": "yourmom@choretracker.com",
    },
)

origins = ["*"] # not needed for this project (no front end)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# only including routers needed for Flow #1
app.include_router(chore.router)
app.include_router(roommate.router)
app.include_router(chore_assignment.router)


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to the Chore Tracker API."}
