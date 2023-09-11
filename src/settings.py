from pydantic import BaseSettings


class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    SUPERUSER_USERNAME: str
    SUPERUSER_PASSWORD: str

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
