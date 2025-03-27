#!/usr/bin/env python3
"""
YouTube Comments Feeling Analyzer

This is the main entry point for the YouTube Comments Feeling Analyzer application.
It can be run in two modes:
1. As a command-line tool to analyze a specific video
2. As a web server to provide an API for analyzing videos

Usage:
    # Run as a command-line tool
    python main.py --video https://www.youtube.com/watch?v=VIDEO_ID
    
    # Run as a web server
    python main.py --server [--port PORT]
"""

import argparse
import os
import sys
import dotenv
import uvicorn

from youtube_analyzer.analyzer.sentiment_analyzer import CommentAnalyzer
from youtube_analyzer.api.app import create_app

# Load environment variables
dotenv.load_dotenv()


def analyze_video(video_url: str) -> None:
    """
    Analyze a YouTube video and print the results.
    
    Args:
        video_url: URL of the YouTube video to analyze.
        
    Returns:
        None
    """
    try:
        analyzer = CommentAnalyzer()
        result = analyzer.analyze(video_url)
        
        print("\n=== Analysis Results ===\n")
        for message in result['messages']:
            message.pretty_print()
            print("\n" + "-"*50 + "\n")
    except Exception as e:
        print(f"Error analyzing video: {e}")
        sys.exit(1)


def run_server(port: int = 8000) -> None:
    """
    Run the API server.
    
    Args:
        port: Port to run the server on.
        
    Returns:
        None
    """
    try:
        uvicorn.run(
            create_app(), 
            host="0.0.0.0", 
            port=port,
            factory=True
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)


def main() -> None:
    """
    Main entry point for the application.
    
    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="YouTube Comments Feeling Analyzer")
    
    # Create mutually exclusive group for the different modes
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--video", 
        type=str, 
        help="URL of the YouTube video to analyze"
    )
    mode_group.add_argument(
        "--server", 
        action="store_true", 
        help="Run as a web server"
    )
    
    # Additional arguments
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to run the server on (default: 8000)"
    )
    
    args = parser.parse_args()
    
    # Check for required environment variables
    if not os.getenv("YOUTUBE_API_KEY"):
        print("Error: YOUTUBE_API_KEY environment variable is not set")
        sys.exit(1)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set")
        sys.exit(1)
    
    # Run in the appropriate mode
    if args.video:
        analyze_video(args.video)
    elif args.server:
        run_server(args.port)


if __name__ == "__main__":
    main()
