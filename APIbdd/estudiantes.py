from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator, ConfigDict
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os
import certifi  # <-- EL SALVAVIDAS DE SEGURIDAD SSL

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB", "Actividad1_noSQL")
COLL_ESTUDIANTES = os.getenv("COLL_ESTUDIANTES", "estudiantes")

client: AsyncIOMotorClient | None = None
db = None
estudiantes_coll = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db, estudiantes_coll
    # Lógica de Startup con validación SSL forzada
    client = AsyncIOMotorClient(MONGODB_URI, tlsCAFile=certifi.where())
    db = client[DB_NAME]
    estudiantes_coll = db[COLL_ESTUDIANTES]
    print("Conexión a MongoDB Atlas establecida exitosamente (SSL Validado).")

    yield

    if client:
        client.close()
        print("Conexión a MongoDB cerrada de forma segura.")

app = FastAPI(title="API con FastAPI y MongoDB Atlas", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EstudianteIn(BaseModel):
    nombre: str
    email: str
    carrera: str
    semestre: int

class EstudianteOut(EstudianteIn):
    id: str = Field(alias="_id")

    @field_validator("id", mode="before")
    def objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

@app.get("/")
def home():
    return {"mensaje": "API conectada a MongoDB Atlas funcionando al 100%"}

@app.get("/estudiantes", response_model=list[EstudianteOut])
async def listar_estudiantes(
        skip: int = Query(0, description="Registros a omitir"),
        limit: int = Query(50, le=100, description="Límite de registros (máx 100)")
):
    return [EstudianteOut(**d) async for d in estudiantes_coll.find({}).skip(skip).limit(limit)]

@app.get("/estudiantes/{id}", response_model=EstudianteOut)
async def obtener_estudiante(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido.")
    doc = await estudiantes_coll.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
    return EstudianteOut(**doc)

@app.post("/estudiantes", response_model=EstudianteOut, status_code=status.HTTP_201_CREATED)
async def crear_estudiante(e: EstudianteIn):
    result = await estudiantes_coll.insert_one(e.model_dump())
    nuevo = await estudiantes_coll.find_one({"_id": result.inserted_id})
    return EstudianteOut(**nuevo)

@app.put("/estudiantes/{id}", response_model=EstudianteOut)
async def actualizar_estudiante(id: str, e: EstudianteIn):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido.")
    result = await estudiantes_coll.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": e.model_dump()},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
    return EstudianteOut(**result)

@app.delete("/estudiantes/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_estudiante(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido.")
    result = await estudiantes_coll.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
    return None

@app.get("/app")
def app_ui():
    return FileResponse("static/index.html")