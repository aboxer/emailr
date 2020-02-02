#from __future__ import print_function
import pickle
import os.path
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
import sys
import json
import time
import datetime

# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def create_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  #return {'raw': base64.urlsafe_b64encode(message.as_string())}
  foo = base64.urlsafe_b64encode(message.as_bytes())
  foo = foo.decode()
  return{'raw': foo}
  #return {'raw': base64.urlsafe_b64encode(message.as_bytes())}


def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except HttpError as error:
    print('An error occurred: %s' % error)


def str2ts(s):
  t = time.mktime(datetime.datetime.strptime(s, "%m/%d/%Y").timetuple())
  return int(t)

def prStats(db):
  lastGv = 0
  lastRq = 0
  totAmt = 0.0
  giversCt = 0
  for rec in db:
    if 'lastGv' in rec and rec['lastGv'] > lastGv:
      lastGv = rec['lastGv']
    if 'lastRq' in rec and rec['lastRq'] > lastRq:
      lastRq = rec['lastRq']
    if 'totAmt' in rec and rec['totAmt'] != 0.0:
      giversCt += 1
      totAmt += rec['totAmt']
    print(rec)

  print('curTime = ',datetime.datetime.fromtimestamp(int(time.time())))
  print('lastGv = ',datetime.datetime.fromtimestamp(lastGv))
  print('lastRq = ',datetime.datetime.fromtimestamp(lastRq))
  print('totAmt = ',totAmt)
  print('giversCt = ',giversCt)
  print('emailSz = ',len(db))
#srv = create_service()
#msg = create_message('aaron.boxer@gmail.com','aboxer51@yahoo.com','test','test message profile.pmc.org/AB0492')
#send_message(srv,'me',msg)

