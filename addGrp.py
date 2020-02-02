import sys
import json
import time
import datetime

def str2ts(s):
  t = time.mktime(datetime.datetime.strptime(s, "%m/%d/%Y").timetuple())
  return int(t)

emailDb = 'data/emailDb.json'
dbf = open(emailDb, 'r')
r = dbf.read()  #read in all the bytes into one string
db = json.loads(r)

grp = sys.argv[1]
inf = open(sys.argv[2],'r')
for line in inf:
  dat = line.split(',')
  fullNm = dat[0].strip()
  email = dat[1].strip()
  for rec in db:
    if email == rec['email']:  #ignore duplicates
      break
  else:  #add a record - other fields will be added by other tools
    newRec = {}
    newRec['fullNm'] = fullNm
    newRec['email'] = email
    newRec['grp'] = grp
    db.append(newRec)

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

outf = open(emailDb,'w') #rewrite the database
json.dump(db,outf)
