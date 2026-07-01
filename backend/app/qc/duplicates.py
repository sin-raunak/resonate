# duplicates.py

import acousticid 
from app.config import settings 
from app.models.schemas import QCStatus, ReasonCode, QCCheckResult
from app.qc.integrity import md5_hash 

def check_exact_duplicates(filepath: str, seen_hashes: dict[str, str]) -> QCCheckResult:
    file_hash = md5_hash(filepath)

    if file_hash in seen_hashes: 
        return QCCheckResult(
            check_name="duplicate_exact", 
            status=QCStatus.FAIL, 
            reason_code=ReasonCode.DUPLICATE, 
            details=f"Exact duplicate of {seen_hashes[file_hash]}"
        )
    
    seen_hashes[file_hash] = filepath
    return QCCheckResult(
        check_name="duplicate_exact", 
        status=QCStatus.PASS, 
    )

def get_fingerprint(filepath: str) -> str:
    duration, fingerprint = acoustid.fingerprint_file(file_path)
    return fingerprint 

def _fingerprint_similarity(fp1: str, fp2: str) -> float:
    matches = sum(1 for a, b in zip(fp1, fp2) if a == b)
    return matches / max(len(fp1), len(fp2))

def check_near_duplicates(filepath: str, seen_fingerprints: dict[str, str]) -> QCCheckResult:
    try:
        fp = get_fingerprint(filepath)
    except Exception as e: 
        return QCCheckResult(
            check_name="duplicate_near", 
            status=QCStatus.REVIEW, 
            details=f"Fingerprinting failed: {e}"
        )
    
    for clip_id, other_fp in seen_fingerprints.items():
        similarity = _fingerprint_similarity(fp, other_fp)
        if similarity > settings.duplicate_fingerprint_similarity:
            return QCCheckResult(
                check_name="duplicate_near",
                status=QCStatus.REVIEW,
                score=similarity,
                reason_code=ReasonCode.DUPLICATE,
                details=f"Fingerprint similarity {similarity:.2f} with clip {clip_id}",
            )
    
    return QCCheckResult(check_name="duplicate_near", status=QCStatus.PASS)
