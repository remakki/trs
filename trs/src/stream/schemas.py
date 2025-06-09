from typing import TypedDict


class Message(TypedDict):
    content: str
    start: float
    end: float
