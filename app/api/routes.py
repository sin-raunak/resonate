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
async def run_qc(files: list[UploadFile] = File(...)):
    """
    Accepts audio files, builds manifest rows on the fly (no text/language yet),
    runs pipeline, returns QC reports.
    NOTE: proposed_text/language are placeholders until we wire the manifest CSV upload.
    """
    manifest_rows = []

    for f in files:
        clip_id = str(uuid.uuid4())
        save_path = os.path.join(UPLOAD_DIR, f"{clip_id}_{f.filename}")

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)

        manifest_rows.append(
            ManifestRow(
                clip_id=clip_id,
                vendor_id="8e2f00f1-fa60-431b-a9c0-99ecd9a4c527",
                filepath=save_path,
                clip_type= "TTS",
                proposed_text="",   
                language="unknown", 
            )
        )
    
    reports = run_pipeline(manifest_rows)
    return JSONResponse(
        content=[r.model_dump(mode="json") for r in reports]
    )