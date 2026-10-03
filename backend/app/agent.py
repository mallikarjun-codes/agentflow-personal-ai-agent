import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.tools.web_search import web_search
from app.tools.gmail import send_email
from app.tools.calendar import (
    list_events,
    create_event,
    update_event,
    delete_event,
)

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY"),
)

agent = create_agent(
    model=model,
    tools=[
        web_search,
        send_email,
        list_events,
        create_event,
        update_event,
        delete_event,
    ],
    system_prompt=(
        "You are AgentFlow, a personal AI assistant. "
        "Use tools whenever the user asks you to perform an action "
        "or retrieve current information. "
        "Before updating or deleting a calendar event, identify the "
        "correct event using list_events."
    ),
)