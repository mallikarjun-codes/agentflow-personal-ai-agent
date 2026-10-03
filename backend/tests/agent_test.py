from app.agent import agent

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Search the web for the latest developments in AI, "
                    "summarize the important points, and email the summary "
                    "to sarveshmadawal17@gmail.com with subject 'AI Update'."
                ),
            }
        ]
    }
)

print(result["messages"][-1].content)