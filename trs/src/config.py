from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    FLOW: str

    AI_BASE_URL: str
    AI_EMAIL: str
    AI_PASSWORD: str

    TRANSCRIPTION_BASE_URL: str
    TRANSCRIPTION_USERNAME: str
    TRANSCRIPTION_PASSWORD: str

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_QUEUE: str


settings = Settings()
