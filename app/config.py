from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres123@localhost:5432/tooling_db"
    APP_NAME: str = "Tooling Master Records Management"
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
