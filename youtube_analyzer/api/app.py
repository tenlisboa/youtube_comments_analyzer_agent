"""
FastAPI application for the YouTube Comments Feeling Analyzer.
"""

from fastapi import FastAPI

from youtube_analyzer.api.routes import router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI
    """
    app = FastAPI(
        title="YouTube Comments Feeling Analyzer",
        description="API for analyzing the sentiment of YouTube video comments",
        version="1.0.0"
    )
    
    # Add routes
    app.include_router(router)
    
    # Add a root endpoint for health checks
    @app.get("/")
    async def root():
        """Root endpoint for health checks."""
        return {"status": "ok", "message": "YouTube Comments Feeling Analyzer API is running"}
    
    return app
