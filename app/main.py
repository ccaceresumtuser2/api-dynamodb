from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.hoja_vida_controller import router as hoja_vida_router

app = FastAPI(
    title="API Gestión de Usuarios",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hoja_vida_router)


