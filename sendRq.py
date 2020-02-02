import sys
import json
import mailLib
import time

emailDb = 'data/emailDb.json'
dbf = open(emailDb, 'r')
r = dbf.read()  #read in all the bytes into one string
db = json.loads(r)

sendList = []
for i in range(len(db)):
  rec = db[i]
  if 'lastRq' not in rec:
    sendList.append(i)

for i in sendList:
  rec = db[i]
  email = rec['email']
  firstNm = rec['fullNm'].split()[0]   #just first name
  body = firstNm + ' - test message profile.pmc.org/AB0492'
  try:
    sys.argv[1]
    srv = mailLib.create_service()
    msg = mailLib.create_message('aaron.boxer@gmail.com',email,'test',body)
    mailLib.send_message(srv,'me',msg)
    db[i]['lastRq'] = int(time.time())
    if 'rqCt' not in rec:
      db[i]['rqCt'] = 1
    else:
      db[i]['rqCt'] += 1
  except:
    print(email)

mailLib.prStats(db)

outf = open(emailDb,'w') #rewrite the database
json.dump(db,outf)
