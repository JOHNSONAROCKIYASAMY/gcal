from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta


# 1. Load Service Account

scope = ["https://www.googleapis.com/auth/calendar"]

creds = Credentials.from_service_account_file(
    "creds.json",
    scopes=scope
)

API_NAME = "calendar"
API_VERSION = "v3"

service = build(API_NAME, API_VERSION, credentials=creds)


# 2. Your Calendar ID

calendar_id = "afdd4fdc29e84f0465eb0cf57352832fee5ab88d99035bccd74cb592b4076066@group.calendar.google.com"


# 3. FREEBUSY CHECK

time_min = datetime.utcnow()
time_max = time_min + timedelta(hours=20)

payload = {
    "timeMin": time_min.isoformat() + "Z",
    "timeMax": time_max.isoformat() + "Z",
    "items": [{"id": calendar_id}]
}

print("\n FREEBUSY REQUEST ")
print(payload)

freebusy = service.freebusy().query(body=payload).execute()
print("\n FREEBUSY RESULT ")
print(freebusy)

'''
# 4. INSERT EVENT

start = datetime.utcnow()
end = start + timedelta(hours=1)

event = {
    "summary": "Test Summary",
    "description": "Description test",
    "start": {
        "dateTime": start.isoformat() + "Z",
    },
    "end": {
        "dateTime": end.isoformat() + "Z",
    },
    "reminders": {
        "useDefault": False,
        "overrides": [
            {"method": "popup", "minutes": 30},
        ],
    },
}

created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

print("\n EVENT CREATED ")
print(created_event)
'''
# 5. LIST EVENTS (for deleting)

events_result = service.events().list(
    calendarId=calendar_id,
    timeMin=time_min.isoformat() + "Z",
    timeMax=time_max.isoformat() + "Z",
    singleEvents=True,
    orderBy="startTime"
).execute()

events = events_result.get("items", [])

print("\n EVENTS FOUND ")
print(events)


# 6. DELETE EVENTS

print("\n DELETING EVENTS ")
for reservation in events:
    event_id = reservation["id"]
    summary = reservation.get("summary", "No Title")

    print(f"Deleting: {summary} (ID: {event_id})")

    service.events().delete(
        calendarId=calendar_id,
        eventId=event_id
    ).execute()

print("\n ALL EVENTS DELETED SUCCESSFULLY ")
