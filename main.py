import dotenv
import os
from langchain_openai import ChatOpenAI
from googleapiclient.discovery import build 
from comentary_extractor import CommentExtractor, CommentExtractorResponse
from langgraph.graph import MessagesState
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from IPython.display import Image, display

dotenv.load_dotenv()

llm = ChatOpenAI(model='gpt-4o')

def comentaries(video_url: str, next_page_token: str | None = None) -> CommentExtractorResponse:
    """
    Extracts the comments from a YouTube video given its URL.

    Args:
        video_url: (str) The URL of the YouTube video.
        next_page_token: (str | None) The token for pagination, if provided search the next commentaries

    Returns:
        ComentExtractorResponse: A dict containing the comments and next_page_token (can be None).
    """

    youtube = build('youtube', 'v3', developerKey=os.getenv("YOUTUBE_API_KEY"))
    extractor = CommentExtractor(
        video_url,
        youtube=youtube
    )
    response = extractor.extract(next_page_token)

    return response

tools = [comentaries]
chat = llm.bind_tools(tools)

SYSTEM = SystemMessage(content="You are an Digital Marketeer tasked with the activity to extract the feeling of a youtube video commentaries. If you need more comentaries you are an Digital Marketeer")

def assistant(state: MessagesState):
    return {"messages": [
        chat.invoke([SYSTEM] + state["messages"])
    ]}

builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition
)

builder.add_edge("tools", "assistant")

graph = builder.compile()

# display(Image(graph.get_graph(xray=True).draw_mermaid_png()))

messages = [HumanMessage(content="Poderia analizar os comentários desse vídeo: https://www.youtube.com/watch?v=ML8h9pgWyXw")]
messages = graph.invoke({"messages": messages})

for m in messages['messages']:
    m.pretty_print()
