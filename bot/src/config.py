from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    CHANNEL_NAME: str

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_QUEUE: str

    class Config:
        env_file = ".env"


settings = Settings()
