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
import csv
import time
import datetime
import msgMkr
import re
from tabulate import tabulate

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
  def __init__(self,db):
    self.db = db
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
    for msg in msgList:
      try:
        messagstorye = (self.service.users().messages().send(userId="me", body=msg[1]).execute())
        idx = msg[0]
        rec = self.db.getRec(idx)
        rec['lastRq'] = int(time.time())
        if rec['rqCt'] == None:
          rec['rqCt'] = 1
        else:
          rec['rqCt'] += 1
        self.db.setRec(idx,rec)
      except HttpError as error:
        print('An error occurred: %s' % error)

###################### stuff related to database model class ###############################

#convert a month/day/year string into a unix time stamp
def str2ts(x):
  if re.search(':',x) == None: #colons indicates exact time
    t = time.mktime(datetime.datetime.strptime(x, "%m/%d/%Y").timetuple())
  else:
    t = time.mktime(datetime.datetime.strptime(x, "%m/%d/%Y %H:%M:%S").timetuple())
  #t = time.mktime(datetime.datetime.strptime(x, "%m/%d/%Y %H:%M:%S").timetuple())
  return int(t)

#convert csv file to database
def csv2db(infile):
  db = []
  with open(infile, newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    flag = False
    for row in spamreader:
      row = [x.strip(' ') for x in row] #strip white space from each element in row
      if flag == False:
        cols = row
        flag = True
      else:
        rec = {}
        for col in cols:
          val = row.pop(0)
          if val == '':
            val = None
          else:
            if col == 'lastRq' or col == 'lastGv': #convert PMC format(mm/dd/yyyy) to unix timestamp
              val = str2ts(val)
            if col == 'rqCt' or col == 'rqCt': #
              val = int(val)
            elif col == 'totAmt':   
              val = float(val)
            elif col == 'act':   
              if val.lower() == 'true':
                val = True
              else:
                val = False
          rec[col] = val
        db.append(rec)
    return db

#convert database to csv file
def db2csv(db,outfile):
  with open(outfile, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    cols = list(db[0].keys())  #all the rows in the database have the same keys
    spamwriter.writerow(cols)
    for rec in db:
      row = []
      for col in cols:
        val = rec[col]
        if (col == 'lastRq' or col == 'lastGv') and val != None: #convert unix timestamp to mm/dd/yyyy
          val = datetime.datetime.fromtimestamp(val).strftime('%m/%d/%Y %H:%M:%S')
          #val = datetime.date.fromtimestamp(val).strftime('%m/%d/%Y')
        elif col == 'act':   
          if val == True:
            val = 'True'
          else:
            val = 'False'
        row.append(val)
      spamwriter.writerow(row)

#print database to table
def db2Tbl(db):
  cols = list(db[0].keys())  #all the rows in the database have the same keys
  tbl = [cols]
  for rec in db:
    row = []
    for col in cols:
      try:
        val = rec[col]
        if col == 'lastRq' or col == 'lastGv': #convert unix timestamp to mm/dd/yyyy
          val = datetime.datetime.fromtimestamp(val).strftime('%m/%d/%Y %H:%M:%S')
        elif col == 'totAmt':
          val = str(val)
      except:
        val = None
      row.append(val)
    tbl.append(row)
  niceTbl =  tabulate(tbl,headers='firstrow',floatfmt="5.2f")
  #print(niceTbl)
  return niceTbl 

 

#email database class
class emailDb:
  def __init__(self,emailDb):
    #open existing database or create a new one
    #The database csv must have all the columns filled even if some are filled with None
    self.dbNm = emailDb
    self.dbCols = ['fullNm','email','grp','rqCt','lastRq','gvCt','lastGv','totAmt','act']
    try:
      self.db = csv2db(self.dbNm)
      #dbf = open(self.dbNm, 'r')
      #r = dbf.read()  #read in all the bytes into one string
      #self.db = json.loads(r)
      #dbf.close()
    except: #create empty file for database
      self.db = []
      nf = open(self.dbNm,'w')
      nf.close()

  #write out the database
  def exitDb(self):
    #The database csv must have all the columns filled even if some are filled with None
    db2csv(self.db,self.dbNm) #NOTE: Add backup to dropbox
    #dbf = open(self.dbNm, 'w')
    #json.dump(self.db,dbf)
    #dbf.close()

  #get record
  def getRec(self,idx):
    return self.db[idx]

  #set record
  def setRec(self,idx,rec):
    self.db[idx] = rec

  def emptyRec(self):
    rec = {}
    for col in self.dbCols:
      rec[col] = None
    return rec
  
  #get database stats
  def prStats(self):
    lastGv = 0
    lastRq = 0
    totAmt = 0.0
    giversCt = 0
    for rec in self.db:
      if rec['lastGv'] != None and rec['lastGv'] > lastGv:
        lastGv = rec['lastGv']
      if rec['lastRq'] != None and rec['lastRq'] > lastRq:
        lastRq = rec['lastRq']
      if rec['totAmt'] != None and rec['totAmt'] != 0.0:
        giversCt += 1
        totAmt += rec['totAmt']
      #print(rec)

    print('curTime = ',datetime.datetime.fromtimestamp(int(time.time())))
    print('lastGv = ',datetime.datetime.fromtimestamp(lastGv))
    print('lastRq = ',datetime.datetime.fromtimestamp(lastRq))
    print('totAmt = ',totAmt)
    print('giversCt = ',giversCt)
    print('emailSz = ',len(self.db))


  #initialize database with existing records
  def setDb(self,setList):
    try:
      rows = csv2db(setList)
      #inf = open(setList,'r')
    except:
      return 'ERR - not found ' + setList

    #any non-existing fields are set to a default
    for row in rows:
      for rec in self.db:
        if row['email'] == rec['email']:  #ignore duplicates
          break
      else:
        self.db.append(row)

  #add new email address to database
  def addGrp(self,grp,fileNm):
    try:
      #inf = open(args[2],'r')
      adds = csv2db(fileNm)
    except:
      return 'ERR - not found ' + args[2]

    for add in adds:
      for rec in self.db:
        if add['email'] == rec['email']:  #ignore duplicates
          break
      else:  #add a record - other fields will be added by other tools
        newRec = self.emptyRec()
        newRec['fullNm'] = add['fullNm']
        newRec['email'] = add['email']
        newRec['act'] = True
        newRec['grp'] = grp
        self.db.append(newRec)

  #remove records from database
  def rmRec(self,arg):
    try:
      rmvs = csv2db(arg)
    except:
      return 'ERR - not found ' + args[1]

    for rmv in rmvs:
      email = rmv['email']
      for i in range(len(self.db)):
        rec = self.db[i]
        if email == rec['email'] and rec['lastGv'] == None :  #this email has never given
          self.db.pop(i)
          break


  #get request list
  def getRqs(self):
    sendList = []
    for i in range(len(self.db)):
      rec = self.db[i]
      if rec['act'] == True and rec['lastRq'] == None:
        sendList.append(i)

    msgList = []
    for i in sendList:
      rec = self.db[i]
      email = rec['email']
      firstNm = rec['fullNm'].split()[0]   #just first name
      #print(rec['fullNm'],email)
      #body = firstNm + ' - test message profile.pmc.org/AB0492'
      #body = messages.msgs['tsg_rq1']
      body = msgMkr.mkMsg('tsg_rq1',rec)
      msg = create_message('aaron.boxer@gmail.com',email,'test',body)
      msgList.append((i,msg))
    return sendList,msgList

  def prTbl(self):
#    cols = ['fullNm','email','grp','rqCt','lastRq','gvCt','lastGv','totAmt','act']
#    tbl = [cols]
#    for rec in self.db:
#      row = []
#      for key in cols:
#        try:
#          val = rec[key]
#        except:
#          val = None
#        if key == 'lastRq' or key == 'lastGv' and val != None:
#          #row.append(datetime.datetime.fromtimestamp(val))
#          row.append(datetime.date.fromtimestamp(val))
#        else:
#          row.append(val)
#      tbl.append(row)
    #niceTbl =  tabulate(tbl,headers='firstrow')
    niceTbl =  db2Tbl(self.db)
    print(niceTbl)



