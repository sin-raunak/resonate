# pipeline.py 

from app.models.schemas import ManifestRow, ClipQCReport, QCStatus
from app.qc.silence import check_silence 
from app.qc.integrity import check_integrity, md5_hash
from app.qc.duplicates import check_exact_duplicates, check_near_duplicates
from app.qc.text_audio_match import check_text_audio_match


def run_pipeline(manifest_rows: list[ManifestRow]) -> list[ClipQCReport]:
    seen_hashes: dict[str, str] = {}
    seen_fingerprints: dict[str, str] = {}
    all_texts = [manifest_row.proposed_text for manifest_row in manifest_rows]
    reports: list[ClipQCReport] = []

    for row in manifest_rows: 
        report = ClipQCReport(clip_id=row.clip_id, filepath=row.filepath)

        # QC 1: Integrity (escape if failed)
        integrity_result = check_integrity(row.filepath)
        report.checks.append(integrity_result)

        if integrity_result.status == QCStatus.FAIL:
            report.final_status = QCStatus.FAIL
            report.excluded = True
            reports.append(report)
            continue 
        
        # QC 2: Silence (escape if failed)
        silence_result = check_silence(row.filepath)
        report.checks.append(silence_result)

        if silence_result.status == QCStatus.FAIL:
            report.final_status = QCStatus.FAIL
            report.excluded = True
            reports.append(report)
            continue
        
        # QC 3: Exact Duplicates (escape if failed)
        exact_dup_result = check_exact_duplicates(row.filepath, row.clip_id, seen_hashes)
        report.checks.append(exact_dup_result)

        if exact_dup_result.status==QCStatus.FAIL:
            report.final_status = QCStatus.FAIL
            report.excluded = True
            reports.append(report)
            continue 
        
        # QC 4: Near Duplicates 
        near_dup_result = check_near_duplicates(row.filepath, row.clip_id, seen_fingerprints)
        report.checks.append(near_dup_result)

        if near_dup_result.status == QCStatus.REVIEW: 
            report.final_status = QCStatus.REVIEW
            report.flags.append("Possible duplicate") 
        
        # QC 4: Text Audio Match (using Whisper)
        text_match_result = (row.filepath, row.proposed_text, all_texts):
        report.checks.append(text_match_result)

        if text_match_result.status == QCStatus.FAIL:
            report.final_status = QCStatus.FAIL
            report.excluded = True
            reports.append(report)
            continue
        
        reports.append(report)
    
    return reports