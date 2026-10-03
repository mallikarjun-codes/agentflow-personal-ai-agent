from app.tools.gmail import send_email

result = send_email.invoke({
    "to": "madawalsarvesh@gmail.com",
    "subject": "AgentFlow Test",
    "body": "This is a test email sent by AgentFlow."
})

print(result)