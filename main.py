from typing import List
from uuid import UUID

from fastapi import FastAPI, HTTPException

from models import Gender, Role, User, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("1c64e733-daca-4b1e-820a-1d3cda8813bc"),
        first_name="Ned",
        last_name="Stark",
        gender=Gender.male,
        Roles=[Role.admin, Role.user],
    ),
    User(
        id=UUID("ac0078a5-2de2-4d1e-b8c6-9721fd76091a"),
        first_name="Jon",
        last_name="Snow",
        gender=Gender.male,
        Roles=[Role.student],
    ),
]


@app.get("/")
async def root():
    return {"Hello": "world"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404, detail=f"User with id: {user_id} does not exist"
    )


@app.put("/api/v1/users/{user_id}")
async def update_users(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.Roles is not None:
                user.Roles = user_update.Roles
            return
    raise HTTPException(
        status_code=404, detail=f"User with id: {user_id} does not exist"
    )
