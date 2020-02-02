import sys
import json
import time
import datetime

def str2ts(s):
  t = time.mktime(datetime.datetime.strptime(s, "%m/%d/%Y").timetuple())
  return int(t)

inf = open(sys.argv[1],'r')
db = []
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
  db.append(rec)

outf = open('data/emailDb.json','w')
json.dump(db,outf)

lastGv = 0
lastRq = 0
totAmt = 0.0
giversCt = 0
for rec in db:
  if rec['lastGv'] > lastGv:
    lastGv = rec['lastGv']
  if rec['lastRq'] > lastRq:
    lastRq = rec['lastRq']
  if rec['totAmt'] != 0.0:
    giversCt += 1
    totAmt += rec['totAmt']
  print(rec)

print('curTime = ',datetime.datetime.fromtimestamp(int(time.time())))
print('lastGv = ',datetime.datetime.fromtimestamp(lastGv))
print('lastRq = ',datetime.datetime.fromtimestamp(lastRq))
print('totAmt = ',totAmt)
print('giversCt = ',giversCt)
print('emailSz = ',len(db))

