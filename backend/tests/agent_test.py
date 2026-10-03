from app.agent import agent

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What are the latest developments in AI?"
            }
        ]
    }
)

print(result["messages"][-1].content)