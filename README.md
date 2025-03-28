# YouTube Comments Feeling Analyzer

A powerful tool that uses AI to analyze the sentiment and feelings expressed in YouTube video comments, providing valuable insights for digital marketers and content creators.

## Overview

This project leverages the YouTube Data API to extract comments from videos and uses OpenAI's GPT models through LangChain to analyze the sentiment and overall feeling of the audience. The analysis is structured as an agent-based workflow using LangGraph, allowing for dynamic comment extraction and analysis.

## Features

- Extract comments from any YouTube video using just the URL
- Analyze sentiment and feelings expressed in comments
- Support for pagination to analyze large comment sections
- Handles comment replies for comprehensive analysis
- Agent-based architecture for intelligent analysis flow
- REST API for integration with other systems
- Docker support for easy deployment

## Requirements

- Python 3.8+
- YouTube Data API key
- OpenAI API key
- Docker (optional, for containerized deployment)

## Installation

### Local Development

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd youtube_comments_analyzer_agent
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Copy `.env.example` to `.env` (or create a new `.env` file)
   - Fill in your API keys:
     ```
     YOUTUBE_API_KEY=your_youtube_api_key
     OPENAI_API_KEY=your_openai_api_key
     ```

### Docker Deployment

1. Make sure Docker and Docker Compose are installed on your system

2. Set up your environment variables in the `.env` file as described above

3. Build and start the Docker container:

   ```bash
   docker-compose up -d
   ```

## Usage

### Running Locally

#### Command Line

Run the main script to analyze a YouTube video:

```bash
python main.py --video "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

#### API Server

Start the API server:

```bash
python main.py --server --port 8000
```

The API will be available at http://localhost:8000

### Using the API

Once the API is running (either locally or via Docker), you can use it to analyze YouTube videos:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"video_url": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"}'
```

Or using Python requests:

```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={"video_url": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"}
)

print(response.json())
```

## Project Structure

```
.
├── main.py                        # Main entry point for CLI and API
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose configuration
├── requirements.txt               # Python dependencies
└── youtube_analyzer/             # Main package
    ├── __init__.py
    ├── api/                       # API module
    │   ├── __init__.py
    │   ├── app.py                 # FastAPI application
    │   └── routes.py              # API routes
    ├── analyzer/                  # Analysis module
    │   ├── __init__.py
    │   └── sentiment_analyzer.py  # Comment sentiment analysis
    ├── client/                    # YouTube client module
    │   ├── __init__.py
    │   └── youtube_client.py      # YouTube API interaction
    └── models/                    # Data models
        ├── __init__.py
        ├── comment.py             # Comment data model
        └── response.py            # Response data models
```

## How It Works

1. The system takes a YouTube video URL as input (via CLI or API)
2. The `CommentExtractor` extracts comments using the YouTube Data API
3. The `CommentAnalyzer` processes these comments using LangChain and GPT-4o
4. The AI analyzes the sentiment and feelings expressed in the comments
5. Results are returned via the console or API response

## Class Structure

- `YouTubeClient`: Handles YouTube API authentication and client creation
- `CommentExtractor`: Extracts comments from YouTube videos
- `Comment`: Data model for YouTube comments
- `CommentExtractorResponse`: Data model for extraction responses
- `AnalysisResult`: Data model for analysis results
- `CommentAnalyzer`: Analyzes comments using LangChain and GPT

## Extending the Project

You can extend this project by:

- Adding visualization of sentiment analysis results
- Implementing comment filtering by criteria
- Creating a web UI for easier interaction
- Adding support for batch processing of multiple videos
- Exporting analysis results to various formats
- Adding authentication to the API

## Acknowledgments

- This project uses the YouTube Data API
- Powered by OpenAI's GPT models through LangChain
- Built with LangGraph for agent-based workflows
- API built with FastAPI
