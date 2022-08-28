from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_calendar_event():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        now = datetime.datetime.utcnow()
        end_time = now + datetime.timedelta(hours=1)

        event = {
            'summary': 'Lunch Break - Out Off Office',
            'start': {
                'dateTime': now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'timeZone': 'America/Sao_Paulo',
            },
            'reminders': {
                'useDefault': True,
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)
