from fastapi import FastAPI, Path, status, Body, HTTPException
from typing import Annotated
from pydantic import BaseModel
from typing import List

app = FastAPI()


class User(BaseModel):
    id: int = None
    username: str
    age: int


users = []


@app.get("/users")
async def get_users_list() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def user_registration(
                            username: Annotated[str, Path(min_length=5, max_length=20,
                                                          description='Enter username', example='UrbanUser')],
                            age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    list_id = []
    if users:
        for user in users:
            list_id.append(user.id)
        user_id = max(list_id) + 1
    else:
        user_id = 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
        username: Annotated[str, Path(min_length=5, max_length=20,
                                      description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}')
async def user_deleter(
        user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]) -> User:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")
