"""
Comment model for YouTube comments.
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Comment:
    """Represents a YouTube comment with its metadata and replies."""
    id: str
    text: str
    user_name: str
    date: str
    replies: List[str] = None
    
    def __post_init__(self):
        """Initialize default values and validate data."""
        if self.replies is None:
            self.replies = []
    
    @property
    def parsed_date(self) -> Optional[datetime]:
        """
        Parse the date string into a datetime object.
        
        Returns:
            Optional[datetime]
        """
        try:
            return datetime.fromisoformat(self.date.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return None
    
    def to_dict(self) -> dict:
        """
        Convert the comment to a dictionary.
        
        Returns:
            dict
        """
        return {
            "id": self.id,
            "text": self.text,
            "user_name": self.user_name,
            "date": self.date,
            "replies": self.replies
        }
