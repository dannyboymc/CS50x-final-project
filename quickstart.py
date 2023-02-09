from __future__ import print_function

import datetime
import os.path
import time

from dateutil import parser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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

    while True:
        try:
            bin = (event(creds))
            time.sleep(1)

            if bin == None:
                continue
            else:
                if 'Green Bin' in bin:
                    print('Green LED')
                if 'Purple Bin' in bin:
                    print('Purple LED')
                if 'Yellow Bin' in bin:
                    print('Yellow LED')

        except KeyboardInterrupt:
            break
        
# calls google calender and returns if event is on now and their discription      
def event(creds):
    bin = ''

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'  # 'Z' indicates UTC time
        # print('Getting the upcoming event')
        events_result = service.events().list(calendarId='e2a46dd1503e96aa0030939fe78797edbe9722121695773e7f74ef153f718147@group.calendar.google.com', timeMin=now, 
                                                maxResults=2, singleEvents=True,
                                                orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            #converts event times to datetime format
            start_time = parser.isoparse(start)
            end_time = parser.isoparse(end)
            now_formatted = parser.isoparse(now)
            
            # check if event is happening now
            if start_time <= now_formatted <= end_time:
                bin += event['summary']      
            else:
                continue
        return bin
        
    except HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    main()
    