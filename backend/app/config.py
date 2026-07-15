# config.py 

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Slience check 
    silence_rms_thresh: float = 0.01
    duplicate_fingerprint_similarity: float = 0.8
    text_match_pass_thresh: float = 80
    text_match_review_low_thresh: float = 60

    class Config:
        env_file = ".env"

settings = Settings()