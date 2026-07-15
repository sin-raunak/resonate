# text_audio_match.py

import whisper 
from fuzzywuzzy import fuzz
from app.config import settings 
from app.models.schemas import QCStatus, ReasonCode, QCCheckResult

_model = None 

def _get_model():
    global _model 
    if _model is None: 
        _model = whisper.load_model("base")
    
    return _model 

def check_text_audio_match(filepath: str, proposed_text: str, all_texts: list[str]) -> QCCheckResult:
    model = _get_model()
    try:
        result = model.transcribe(filepath, fp16=False)
        transcribed_text = result.get("text", "")
    except Exception as e:
        return QCCheckResult(
            check_name="text_audio_match",
            status=QCStatus.FAIL,
            reason_code=ReasonCode.CORRUPT,
            details=f"Whisper transcription failed: {e}"
        )
    
    base_score = fuzz.ratio(transcribed_text.lower(), proposed_text.lower())

    # Check score against all texts
    best_score = base_score 
    best_match_text = proposed_text
    for text in all_texts: 
        score = fuzz.ratio(transcribed_text.lower(), text.lower())
        if score > best_score:
            best_score = score 
            best_match_text = text 
    
    if base_score > settings.text_match_pass_thresh:
        return QCCheckResult(
            check_name="text_audio_match",
            status=QCStatus.PASS,
            score=base_score,
        )
    
    if best_score > settings.text_match_pass_thresh and best_match_text != proposed_text:
        return QCCheckResult(
            check_name="text_audio_match",
            status=QCStatus.FAIL,
            score=base_score,
            reason_code=ReasonCode.TEXT_AUDIO_MISMATCH,
            details=f"Assigned text scored {base_score}, but transcription matches a different text better (score: {best_score}). Possible broken mapping.",
        )
    
    if best_score >= settings.text_match_review_low_thresh:
        return QCCheckResult(
            check_name="text_audio_match",
            status=QCStatus.REVIEW,
            score=base_score,
            details=f"Score {base_score} in review range. Whisper transcription: \"{transcribed_text}\"",
        )

    return QCCheckResult(
        check_name="text_audio_match",
        status=QCStatus.FAIL,
        score=base_score,
        reason_code=ReasonCode.TEXT_AUDIO_MISMATCH,
        details=f"Score {base_score} below fail threshold. Whisper transcription: \"{transcribed_text}\"",
    )


