"""
Sentiment analyzer for YouTube comments using LangChain and GPT models.
"""

from typing import Dict, List, Optional, Any, Callable

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage
from langgraph.graph import MessagesState, START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode

from youtube_analyzer.client.youtube_client import CommentExtractor, YouTubeClient
from youtube_analyzer.models.response import CommentExtractorResponse, AnalysisResult


class CommentAnalyzer:
    """Analyzes YouTube video comments using LLM."""
    
    def __init__(self, model_name: str = 'gpt-4o'):
        """
        Initialize the comment analyzer.
        
        Args:
            model_name: Name of the LLM model to use.
        """
        self.llm = ChatOpenAI(model=model_name)
        self.system_message = SystemMessage(
            content="You are a Digital Marketer tasked with analyzing the sentiment and feelings "
                   "expressed in YouTube video comments. Extract key insights, identify patterns, "
                   "and summarize the overall sentiment. If you need more comments, you can request them."
        )
        
        # Set up the analysis graph
        self.graph = self._build_analysis_graph()
    
    @staticmethod
    def _get_comments_tool(video_url: str, next_page_token: Optional[str] = None) -> CommentExtractorResponse:
        """
        Tool function to extract comments from a YouTube video.
        
        Args:
            video_url: The URL of the YouTube video.
            next_page_token: The token for pagination, if provided search the next commentaries.
            

        """
        extractor = CommentExtractor(video_url)
        return extractor.extract(next_page_token)
    
    def _build_analysis_graph(self) -> StateGraph:
        """
        Build the LangGraph for comment analysis.
        

        """
        # Create tool for the LLM
        tools = [CommentAnalyzer._get_comments_tool]
        chat = self.llm.bind_tools(tools)
        
        # Define the assistant node function
        def assistant_node(state: MessagesState) -> Dict[str, List[BaseMessage]]:
            return {"messages": [
                chat.invoke([self.system_message] + state["messages"])
            ]}
        
        # Build the graph
        builder = StateGraph(MessagesState)
        
        builder.add_node("assistant", assistant_node)
        builder.add_node("tools", ToolNode(tools))
        
        builder.add_edge(START, "assistant")
        builder.add_conditional_edges(
            "assistant",
            tools_condition
        )
        
        builder.add_edge("tools", "assistant")
        
        return builder.compile()
    
    def analyze(self, video_url: str) -> Dict[str, List[BaseMessage]]:
        """
        Analyze comments from a YouTube video.
        
        Args:
            video_url: URL of the YouTube video to analyze.
            

        """
        messages = [HumanMessage(content=f"Please analyze the comments of this video: {video_url}")]
        return self.graph.invoke({"messages": messages})
    
    def get_analysis_result(self, video_url: str) -> AnalysisResult:
        """
        Get a structured analysis result for a YouTube video.
        
        Args:
            video_url: URL of the YouTube video to analyze.
            

        """
        # Extract video ID for reference
        video_id = YouTubeClient.extract_video_id(video_url)
        
        # Run the analysis
        result = self.analyze(video_url)
        
        # Extract the assistant's final response
        assistant_messages = [msg for msg in result["messages"] if msg.type == "ai"]
        
        if not assistant_messages:
            raise ValueError("Analysis failed to produce results")
        
        return AnalysisResult(
            insights=assistant_messages[-1].content,
            video_id=video_id or "unknown",
        )
