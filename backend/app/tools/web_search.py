import os

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web for current information and return relevant results."""
    response = tavily.search(query=query, max_results=5)

    results = response.get("results", [])

    if not results:
        return "No search results found."

    return "\n\n".join(
        f"Title: {result['title']}\n"
        f"URL: {result['url']}\n"
        f"Content: {result.get('content', '')}"
        for result in results
    )