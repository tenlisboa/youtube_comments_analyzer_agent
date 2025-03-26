from typing import TypedDict
from googleapiclient.discovery import Resource 
import dotenv
import re

YTURL_REGEX = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)(?P<video_id>[\w\-]+)(\S+)?$"

dotenv.load_dotenv()

class Comment(TypedDict):
    id: str
    text: str
    user_name: str
    date: str
    replies: list[str]

class CommentExtractorResponse(TypedDict):
    comments: list[Comment]
    next_page_token: str | None

class CommentExtractor:
    def __init__(self, video_url: str, youtube: Resource):
        self.youtube = youtube
        self.video_id = self.get_id_from_url(video_url)

    def get_id_from_url(self, url: str) -> str | None:
        match = re.search(YTURL_REGEX, url)
        if match:
            return match.groupdict()['video_id']
        return None

    def compose_replies(self, item: dict) -> list[str]:
        if item['snippet']['totalReplyCount'] > 0:
            return [reply['snippet']['textDisplay'] for reply in item['replies']['comments']]
        return []

    def extract_comments(self, items: list[dict]) -> list[Comment]:
        return [Comment(
            id=item['snippet']['topLevelComment']['id'],
            text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
            user_name=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
            date=item['snippet']['topLevelComment']['snippet']['publishedAt'],
            replies=self.compose_replies(item)
        ) for item in items]

    def extract(self, next_page_token: str | None = None) -> CommentExtractorResponse:
        response = self.youtube.commentThreads().list(
            part='snippet,replies',
            maxResults=100,
            videoId=self.video_id,
            textFormat='plainText',
            order='relevance',
            pageToken=next_page_token
        ).execute()

        return CommentExtractorResponse({
            'comments': self.extract_comments(response['items']),
            'next_page_token': response['nextPageToken'] if 'nextPageToken' in response else None
        })
