# silence_tests.py

from app.qc.silence import check_silence
result = check_silence("path/to/clip.wav")
print(result.model_dump(mode="json"))