from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Anveshika: Interactive Living Museum of Indian Heritage"
    VERSION: str = "2.0.0"
    SIH_PROBLEM_STATEMENT: str = "26208"
    CIVILIZATION: str = "Indian Heritage & Indus Valley Civilization"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "anveshika_db"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
