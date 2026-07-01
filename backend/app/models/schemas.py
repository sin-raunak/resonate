# schemas.py 

from pydantic import BaseModel 
from typing import Optional 
from enum import Enum 

# Status 
class QCStatus(str, Enum):
    PASS = "pass"
    REVIEW = "review"
    FAIL = "fail"

# Failure reason code 
class ReasonCode(str, Enum): 
    SILENCE = "silence"
    NONE = "none"
    CORRUPT = "corrupt"

# Manifest rows (clips)
class ManifestRow(BaseModel):
    clip_id: str 
    file_path: str 
    clip_type: str 
    language: str 
    speaker_id: Optional[str] = None 
    speaker_id_inferred: Optional[str] = None

# QC result 
class QCCheckResult(BaseModel): 
    check_name: str 
    status: QCStatus
    reason_code: ReasonCode = ReasonCode.NONE
    score: Optional[float] = None 
    details: Optional[str] = None 