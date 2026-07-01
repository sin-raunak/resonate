# pipeline.py 

from app.models.schemas import ManifestRow, ClipQCReport, QCStatus
from app.qc.silence import check_silence 
from app.qc.integrity import check_integrity, md5_hash
from app.qc.duplicates import check_exact_duplicates, check_near_duplicates


def run_pipeline(manifest_rows: list[ManifestRow]) -> list[ClipQCReport]:
    seen_hashes = dict[str, str] = {}
    seen_fingerprints: dict[str, str] = {}
    reports: list[ClipQCReport] = []

    for row in manifest_rows: 
        report = ClipQCReport(clip_id=row["clip_id"], filepath=row["filepath"])

        # QC 1: Integrity (escape if false)
        integrity_result = check_integrity(row["filepath"])
        report["checks"].append(integrity_result)

        if integrity_result["status"] == QCStatus.FAIL:
            report["final_status"] = QCStatus.FAIL
            report["excluded"] = True
            reports.append(report)
            continue 
        
        # QC 2: Silence 
        silence_result = check_silence(row["filepath"])
        report["checks"].append(silence_result)

        if silence_result["status"] == QCStatus.FAIL:
            report["final_status"] = QCStatus.FAIL
            report["excluded"] = True
            reports.append(report)
            continue
        
        # QC 3: Exact Duplicates 
        exact_dup_result = check_exact_duplicates(filepath=row["filepath"], seen_hashes=seen_hashes)
        

    return reports