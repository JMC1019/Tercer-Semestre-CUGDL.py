from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json, os

app = FastAPI()
DATA_FILE = "estudiantes.json"

class Estudiante(BaseModel):
    id: int
    nombre: str
    email: str
    carrera: str
    semestre: int

def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_datos(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.get("/")
def home():
    return "Hello World"

@app.get("/estudiantes")
def listar_estudiantes():
    return cargar_datos()

@app.get("/estudiantes/{id}")
def read_user(id: int):
    data = cargar_datos()
    for e in data:
        if isinstance(e.get("id"), int) and e["id"] == id:
            return e
    raise HTTPException(status_code=404, detail="Estudiante no encontrado por id")

@app.get("/estudiantes/email/{email}")
def obtener_estudiante(email: str):
    data = cargar_datos()
    for e in data:
        if e["email"] == email:
            return e
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")

@app.post("/estudiantes")
def agregar_estudiante(e: Estudiante):
    data = cargar_datos()
    if any(x["email"] == e.email for x in data):
        raise HTTPException(status_code=400, detail="El estudiante ya existe")
    nuevo_id = max(est["id"] for est in data) + 1 if data else 1
    nuevo_estudiante = e.model_dump()
    nuevo_estudiante["id"] = nuevo_id
    data.append(nuevo_estudiante)
    guardar_datos(data)
    return {"mensaje": "Estudiante agregado correctamente", "data": nuevo_estudiante}

@app.put("/estudiantes/{id}")
def actualizar_estudiante(id: int, e: Estudiante):
    data = cargar_datos()
    for i, est in enumerate(data):
        if isinstance(est.get("id"), int) and est["id"] == id:
            data[i] = e.model_dump()
            data[i]["id"] = id
            guardar_datos(data)
            return {"mensaje": "Estudiante actualizado correctamente", "data": data[i]}
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")

@app.delete("/estudiantes/{id}")
def eliminar_estudiante(id: int):
    data = cargar_datos()
    nueva_lista = [e for e in data if not (isinstance(e.get("id"), int) and e["id"] == id)]
    if len(nueva_lista) == len(data):
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    guardar_datos(nueva_lista)
    return {"mensaje": f"Estudiante con id {id} eliminado correctamente"}

@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}