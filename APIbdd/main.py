from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
@app.get("/")
def home():
    return "Hello World"

@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}

@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}

class User(BaseModel):
    name: str
    age: int

users_db = []
@app.post("/users")
def create_user(user: User):
    users_db.append(user.dict())
    return {"message": "Usuario creado", "data": user}

@app.get("/users")
def list_users():
    return users_db