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

###################### stuff related to gmail model class ###############################
# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

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



class gmailr:
  def __init__(self):
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

    self.service = build('gmail', 'v1', credentials=creds)


  def send_message(self, msgList):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    dnList = []
    for msg in msgList:
      try:
        message = (self.service.users().messages().send(userId="me", body=msg[1]).execute())
        #print('Message Id: %s' % message['id'])
        dnList.append((msg[0],int(time.time())))
        #return message
      except HttpError as error:
        print('An error occurred: %s' % error)
    return dnList

###################### stuff related to database model class ###############################

#convert a month/day/year string into a unix time stamp
def str2ts(s):
  t = time.mktime(datetime.datetime.strptime(s, "%m/%d/%Y").timetuple())
  return int(t)

#email database class
class emailDb:
  def __init__(self,emailDb):
    #open existing database or create a new one
    self.dbNm = emailDb
    try:
      dbf = open(self.dbNm, 'r')
      r = dbf.read()  #read in all the bytes into one string
      self.db = json.loads(r)
      dbf.close()
    except:
      self.db = []

  #write out the database
  def exitDb(self):
    dbf = open(self.dbNm, 'w')
    json.dump(self.db,dbf)
    dbf.close()
  
  #get database stats
  def prStats(self):
    lastGv = 0
    lastRq = 0
    totAmt = 0.0
    giversCt = 0
    for rec in self.db:
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
    print('emailSz = ',len(self.db))


  #initialize database with existing records
  def setDb(self,setList):
    try:
      inf = open(setList,'r')
    except:
      return 'ERR - not found ' + setList

    for line in inf:
      rec = {}
      dat = line.split(',')
      rec['fullNm'] = dat[0].strip()
      rec['email'] = dat[1].strip()
      rec['grp'] = dat[2].strip()
      rec['rqCt'] = int(dat[3].strip())
      rec['lastRq'] = str2ts(dat[4].strip())
      rec['totAmt'] = float(dat[5].strip())
      rec['lastGv'] = str2ts(dat[6].strip())
      rec['gvCt'] = int(dat[7].strip())
      self.db.append(rec)
  

  #add new email address to database
  def addGrp(self,args):
    grp = args[1]
    try:
      inf = open(args[2],'r')
    except:
      return 'ERR - not found ' + args[2]

    for line in inf:
      dat = line.split(',')
      fullNm = dat[0].strip()
      email = dat[1].strip()
      for rec in self.db:
        if email == rec['email']:  #ignore duplicates
          break
      else:  #add a record - other fields will be added by other tools
        newRec = {}
        newRec['fullNm'] = fullNm
        newRec['email'] = email
        newRec['grp'] = grp
        self.db.append(newRec)

  #remove records from database
  def rmRec(self,args):
    try:
      inf = open(args[1],'r')
    except:
      return 'ERR - not found ' + args[1]

    for line in inf:
      email = line.strip()
      for i in range(len(self.db)):
        rec = self.db[i]
        if email == rec['email'] and 'lastGv' not in rec:  #this email has never given
          self.db.pop(i)
          break


  #get request list
  def getRqs(self):
    sendList = []
    for i in range(len(self.db)):
      rec = self.db[i]
      if 'lastRq' not in rec:
        sendList.append(i)

    msgList = []
    for i in sendList:
      rec = self.db[i]
      email = rec['email']
      firstNm = rec['fullNm'].split()[0]   #just first name
      body = firstNm + ' - test message profile.pmc.org/AB0492'
      msg = create_message('aaron.boxer@gmail.com',email,'test',body)
      msgList.append((i,msg))
    return msgList

  def updRqs(self,updList):
    for upd in updList:
      idx = upd[0]
      rec = self.db[idx]
      self.db[idx]['lastRq'] = upd[1]
      if 'rqCt' not in rec:
        self.db[idx]['rqCt'] = 1
      else:
        self.db[idx]['rqCt'] += 1


#srv = create_service()
#msg = create_message('aaron.boxer@gmail.com','aboxer51@yahoo.com','test','test message profile.pmc.org/AB0492')
#send_message(srv,'me',msg)

