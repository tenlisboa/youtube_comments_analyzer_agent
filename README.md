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

## Requirements

- Python 3.8+
- YouTube Data API key
- OpenAI API key
- Various Python packages (see `requirements.txt`)

## Installation

1. Clone this repository:

   ```
   git clone <repository-url>
   cd youtube_comments_analyzer_agent
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your API keys:
     - `YOUTUBE_API_KEY`: Your YouTube Data API key
     - `OPENAI_API_KEY`: Your OpenAI API key
     - Other optional LangChain/LangSmith keys for tracing (if needed)

## Usage

Run the main script with a YouTube video URL:

```python
python main.py
```

By default, the script analyzes comments from the video URL hardcoded in the `main.py` file. To analyze a different video, modify the URL in the `messages` variable:

```python
messages = [HumanMessage(content="Poderia analizar os comentários desse vídeo: https://www.youtube.com/watch?v=YOUR_VIDEO_ID")]
```

## Project Structure

- `main.py`: The entry point that sets up the LangGraph workflow and processes the YouTube video
- `comentary_extractor.py`: Contains the `CommentExtractor` class that handles YouTube API interaction
- `requirements.txt`: Lists all required Python packages
- `.env.example`: Template for environment variables

## How It Works

1. The system takes a YouTube video URL as input
2. The `CommentExtractor` extracts comments using the YouTube Data API
3. The LangGraph workflow processes these comments using LangChain and GPT-4o
4. The AI analyzes the sentiment and feelings expressed in the comments
5. Results are displayed in the console

## Extending the Project

You can extend this project by:

- Adding visualization of sentiment analysis results
- Implementing comment filtering by criteria
- Creating a web interface for easier interaction
- Adding support for batch processing of multiple videos
- Exporting analysis results to various formats

## Acknowledgments

- This project uses the YouTube Data API
- Powered by OpenAI's GPT models through LangChain
- Built with LangGraph for agent-based workflows
