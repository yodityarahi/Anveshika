from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Bharat Quest: An Interactive Living Museum"
    VERSION: str = "1.0.0"
    SIH_PROBLEM_STATEMENT: str = "26208"
    CIVILIZATION: str = "Indus Valley Civilization (IVC)"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "bharat_quest_db"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
