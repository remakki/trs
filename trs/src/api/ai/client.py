import requests

from src.api.client import BaseClient
from src.config import settings
from src.stream.schemas import Message


class AIClient(BaseClient):
    def __init__(self):
        super().__init__(
            settings.AI_BASE_URL,
            {
                "email": settings.AI_EMAIL,
                "password": settings.AI_PASSWORD,
            },
        )

    def login(self) -> None:
        ENDPOINT = self.base_url + "/api/v1/auths/signin"
        DATA = self.credentials

        response = requests.post(ENDPOINT, json=DATA)
        response.raise_for_status()

        token = response.json()["token"]
        self.headers["Authorization"] = f"Bearer {token}"

    def chat_completions(self, model: str, messages: list[Message]) -> str:
        """
        Get chat completions from the AI service.
        :param model: The model to use for chat completions
        :param messages: The messages to use for chat completions
        :return: The response content from the AI service
        """
        if not self.headers["Authorization"]:
            self.login()

        ENDPOINT = self.base_url + "/api/chat/completions"

        DATA = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": message["content"],
                    "keep-alive": 60,
                }
                for message in messages
            ],
        }

        response = self._post(endpoint=ENDPOINT, json=DATA)
        response.raise_for_status()
        result = response.json()

        return result["choices"][0]["message"]["content"]
