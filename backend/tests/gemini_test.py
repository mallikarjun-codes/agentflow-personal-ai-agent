import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
)

response = model.invoke("who is mahatma gandhi answer in one line")

print("✅ Gemini connected successfully")
print(response.content)