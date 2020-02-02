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

inf = open(sys.argv[1],'r')
for line in inf:
  email = line.strip()
  for i in range(len(db)):
    rec = db[i]
    if email == rec['email'] and 'lastGv' not in rec:  #this email has never given
      db.pop(i)
      break

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
