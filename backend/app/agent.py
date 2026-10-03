import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.tools.web_search import web_search

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
)

agent = create_agent(
    model=model,
    tools=[web_search],
    system_prompt=(
        "You are AgentFlow, a personal AI assistant. "
        "Use the web_search tool when the user needs current information."
    ),
)