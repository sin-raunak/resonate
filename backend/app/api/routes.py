# routes.py 

from fastapi import APIRouter 

from app.models.schemas import ManifestRow
from app.pipeline import run_pipeline

router = APIRouter()

@router.get("/")
def root():
    return {"message": "Resonate backend is live"}

@router.get("/health")
def health():
    return {"status": "ok"}

