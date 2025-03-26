"""
API routes for the YouTube Comments Feeling Analyzer.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from youtube_analyzer.analyzer.sentiment_analyzer import CommentAnalyzer


# Define API models
class VideoAnalysisRequest(BaseModel):
    """Request model for video analysis API."""
    video_url: str


class VideoAnalysisResponse(BaseModel):
    """Response model for video analysis API."""
    insights: str
    video_id: str
    comment_count: int


# Create router
router = APIRouter(tags=["analysis"])


@router.post("/analyze", response_model=VideoAnalysisResponse)
async def analyze_video(request: VideoAnalysisRequest) -> VideoAnalysisResponse:
    """
    Analyze the sentiment of comments from a YouTube video.
    
    Args:
        request: VideoAnalysisRequest containing the video URL.
        
    Returns:
        VideoAnalysisResponse with analysis insights.
        
    Raises:
        HTTPException: If analysis fails.
    """
    try:
        analyzer = CommentAnalyzer()
        result = analyzer.get_analysis_result(request.video_url)
        
        return VideoAnalysisResponse(
            insights=result.insights,
            video_id=result.video_id,
            comment_count=result.comment_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
