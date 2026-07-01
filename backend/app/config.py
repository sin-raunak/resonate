# config.py 

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Slience check 
    silence_rms_thresh: float = 0.01 

    class Config:
        env_file = ".env"

settings = Settings()