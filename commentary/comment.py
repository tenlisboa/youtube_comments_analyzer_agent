from typing import TypedDict

class Comment(TypedDict):
    id: str
    text: str
    user_name: str
    date: str
    replies: list[str]
