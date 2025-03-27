"""
YouTube API client for interacting with the YouTube Data API.
"""

import os
import re
from typing import Optional, List, Dict, Any

from googleapiclient.discovery import build, Resource

from youtube_analyzer.models.comment import Comment
from youtube_analyzer.models.response import CommentExtractorResponse


# Regular expression to extract video ID from YouTube URLs
YTURL_REGEX = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)(?P<video_id>[\w\-]+)(\S+)?$"


class YouTubeClient:
    """Handles YouTube API interactions."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the YouTube client.
        
        Args:
            api_key: YouTube API key. If None, will try to get from environment.
            
        Raises:
            ValueError If the YouTube API key is not provided and not found in environment.
        """
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YouTube API key is required")
        
        self.client = build('youtube', 'v3', developerKey=self.api_key)
    
    def get_client(self) -> Resource:
        """Get the YouTube API client."""
        return self.client
        
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract the video ID from a YouTube URL.
        
        Args:
            url: YouTube video URL.
            
        Returns:
            Optional[str]
        """
        match = re.search(YTURL_REGEX, url)
        if match:
            return match.groupdict()['video_id']
        return None


class CommentExtractor:
    """Class for extracting comments from YouTube videos."""
    
    def __init__(self, video_url: str, youtube_client: Optional[YouTubeClient] = None):
        """
        Initialize the comment extractor.
        
        Args:
            video_url: URL of the YouTube video.
            youtube_client: YouTube API client. If None, a new client will be created.
        
        Raises:
            ValueError If the video ID cannot be extracted from the URL.
        """
        self.youtube_client = youtube_client or YouTubeClient()
        self.youtube = self.youtube_client.get_client()
        self.video_url = video_url
        self.video_id = YouTubeClient.extract_video_id(video_url)
        
        if not self.video_id:
            raise ValueError(f"Could not extract video ID from URL: {video_url}")
    
    def _compose_replies(self, item: Dict[str, Any]) -> List[str]:
        """
        Extract replies from a comment thread item.
        
        Args:
            item: Comment thread item from YouTube API response.
            
        Returns:
            List[str]
        """
        if item['snippet']['totalReplyCount'] > 0 and 'replies' in item:
            return [reply['snippet']['textDisplay'] for reply in item['replies']['comments']]
        return []
    
    def _extract_comments(self, items: List[Dict[str, Any]]) -> List[Comment]:
        """
        Extract comments from YouTube API response items.
        
        Args:
            items: List of comment thread items from YouTube API response.
            
        Returns:
            List[Comment]
        """
        comments = []
        for item in items:
            try:
                comment = Comment(
                    id=item['snippet']['topLevelComment']['id'],
                    text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    user_name=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    date=item['snippet']['topLevelComment']['snippet']['publishedAt'],
                    replies=self._compose_replies(item)
                )
                comments.append(comment)
            except KeyError as e:
                # Skip malformed comments rather than failing the entire extraction
                print(f"Error extracting comment: {e}")
                continue
        
        return comments
    
    def extract(self, next_page_token: Optional[str] = None) -> CommentExtractorResponse:
        """
        Extract comments from the YouTube video.
        
        Args:
            next_page_token: Token for pagination, if provided search the next comments.
            
        Returns:
            CommentExtractorResponse
            
        Raises:
            Exception If the YouTube API request fails.
        """
        try:
            response = self.youtube.commentThreads().list(
                part='snippet,replies',
                maxResults=100,
                videoId=self.video_id,
                textFormat='plainText',
                order='relevance',
                pageToken=next_page_token
            ).execute()
            
            comments = self._extract_comments(response.get('items', []))
            next_token = response.get('nextPageToken')
            
            return CommentExtractorResponse(
                comments=comments,
                next_page_token=next_token
            )
        except Exception as e:
            # Re-raise with more context
            raise Exception(f"Failed to extract comments for video {self.video_id}: {str(e)}") from e
