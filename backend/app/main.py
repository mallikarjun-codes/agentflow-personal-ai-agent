from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import agent

app = FastAPI(title="AgentFlow")


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request.message,
                }
            ]
        }
    )

    final_message = result["messages"][-1].content

    return {
        "response": final_message
    }