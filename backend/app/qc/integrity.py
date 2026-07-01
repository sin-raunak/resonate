# integrity.py

import subprocess
import os 
import hashlib 
import librosa
from app.models.schemas import QCStatus, ReasonCode,QCCheckResult


def check_integrity(filepath: str) -> QCCheckResult: 
    # Zero byte check
    if not os.path.exists(filepath) or os.path.getsize(filepath)==0: 
        return QCCheckResult(
            check_name="integrity", 
            status=QCStatus.FAIL, 
            reason_code=ReasonCode.CORRUPT,
            details=f"File missing or zero bytes"
        )
    # ffprobe check 
    try: 
        result = subprocess.run(
            ["ffprobe", "-v", "error", filepath],
            capture_output=True, 
            text=True, 
            timeout=10,
        )

        if result.returncode !=0:
            return QCCheckResult(
                check_name="integrity",
                status=QCStatus.FAIL, 
                reason_code=ReasonCode.CORRUPT,
                details=f"ffprobe error: {result.stderr.strip()}",
            )
    except Exception as e: 
        return QCCheckResult(
            check_name="integrity",
            status=QCStatus.FAIL, 
            reason_code=ReasonCode.CORRUPT,
            details=f"ffprobe failed to run: {e}",
        )
    
    # librosa load check (later)

    return QCCheckResult(
        check_name="integrity",
        status=QCStatus.PASS, 
    )

def md5_hash(filename: str) -> str: 
    hasher = hashlib.md5()
    with open(filepath, "rb") as f: 
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
