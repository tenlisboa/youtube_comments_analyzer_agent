from googleapiclient.discovery import Resource 
import dotenv
import re
from .commentary_response import CommentExtractorResponse
from .comment import Comment

YTURL_REGEX = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)(?P<video_id>[\w\-]+)(\S+)?$"

dotenv.load_dotenv()

class CommentExtractor:
    def __init__(self, video_url: str, youtube: Resource):
        self.youtube = youtube
        self.video_id = self._get_id_from_url(video_url)

    def _get_id_from_url(self, url: str) -> str | None:
        match = re.search(YTURL_REGEX, url)
        if match:
            return match.groupdict()['video_id']
        return None

    def _compose_replies(self, item: dict) -> list[str]:
        if item['snippet']['totalReplyCount'] > 0:
            return [reply['snippet']['textDisplay'] for reply in item['replies']['comments']]
        return []

    def _extract_comments(self, items: list[dict]) -> list[Comment]:
        return [Comment(
            id=item['snippet']['topLevelComment']['id'],
            text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
            user_name=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
            date=item['snippet']['topLevelComment']['snippet']['publishedAt'],
            replies=self._compose_replies(item)
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
            'comments': self._extract_comments(response['items']),
            'next_page_token': response['nextPageToken'] if 'nextPageToken' in response else None
        })
