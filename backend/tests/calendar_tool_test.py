from app.tools.calendar import create_event

result = create_event.invoke({
    "summary": "AgentFlow Test Event",
    "start_datetime": "2026-10-04T18:00:00+05:30",
    "end_datetime": "2026-10-04T19:00:00+05:30",
})

print(result)