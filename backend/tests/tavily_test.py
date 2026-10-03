import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise ValueError("TAVILY_API_KEY not found in .env")

client = TavilyClient(api_key=api_key)

response = client.search("latest developments in artificial intelligence")

print("✅ Tavily API connected successfully")
print(f"Results found: {len(response.get('results', []))}")

for result in response.get("results", [])[:3]:
    print(result["title"])
    print(result["url"])
    print()