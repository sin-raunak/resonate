# silency.py 

import librosa 
import numpy as np 
from app.config import settings 
from app.models.schemas import QCStatus, ReasonCode, QCCheckResult


def check_silence(filepath: str) -> QCCheckResult:
    try: 
        y, sr = librosa.load(filepath, sr=None)
    except Exception as e: 
        return QCCheckResult(
            check_name="silence",
            status=QCStatus.FAIL,
            reason_code=ReasonCode.CORRUPT, 
            details=f"Could not load audio: {e}",
        )
    
    rms = float(np.sqrt(np.mean(y**2)))

    if rms < settings.silence_rms_thresh:
        return QCCheckResult(
            check_name="silence",
            status=QCStatus.FAIL, 
            reason_code=ReasonCode.SILENCE, 
            score=rms, 
            details=f"RMS {rms:.4f} below threshold of {settings.silence_rms_thresh}"
        )
    
    return QCCheckResult(
        check_name="silence",
        status=QCStatus.PASS, 
        score=rms, 
    )