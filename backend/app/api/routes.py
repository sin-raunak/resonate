# routes.py 

from fastapi import APIRouter 

router = APIRouter()

@router.get("/")
def root():
    return {
        "message": "Resonate backend is live"
    }