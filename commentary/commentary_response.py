from typing import TypedDict
from .comment import Comment

class CommentExtractorResponse(TypedDict):
    comments: list[Comment]
    next_page_token: str | None
