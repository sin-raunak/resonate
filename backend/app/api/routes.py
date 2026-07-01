# routes.py 

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import shutil 
import os 
import uuid 

from app.models.schemas import ManifestRow
from app.pipeline import run_pipeline

router = APIRouter()
UPLOAD_DIR = "upload"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/")
def root():
    return {"message": "Resonate backend is live"}

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/qc/run")
async def run_qc()