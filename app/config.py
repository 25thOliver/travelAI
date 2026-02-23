from pydantic import BaseSettings

class Settings(BaseSettings):
    ollama_base_url: str

    class Config:
        env_file = ".env"

settings = Settings()