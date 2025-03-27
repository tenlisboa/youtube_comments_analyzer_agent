"""
Response models for the YouTube comment extractor.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from .comment import Comment


@dataclass
class CommentExtractorResponse:
    """Response from the comment extractor containing comments and pagination token."""
    comments: List[Comment]
    next_page_token: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the response to a dictionary.
        
        Returns:
            Dict[str, Any]
        """
        return {
            "comments": [comment.to_dict() for comment in self.comments],
            "next_page_token": self.next_page_token
        }


@dataclass
class AnalysisResult:
    """Result of the comment analysis."""
    insights: str
    video_id: str
    comment_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the analysis result to a dictionary.
        
        Returns:
            Dict[str, Any]
        """
        return {
            "insights": self.insights,
            "video_id": self.video_id,
            "comment_count": self.comment_count
        }
