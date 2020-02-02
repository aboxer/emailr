import sys
import json
import mailLib
import time

emailDb = 'data/emailDb.json'
dbf = open(emailDb, 'r')
r = dbf.read()  #read in all the bytes into one string
db = json.loads(r)

inf = open(sys.argv[1],'r')
for line in inf:
  tmp = line.split(',')
  email = tmp[0].strip()
  amt = float(tmp[1].strip())
  for i in range(len(db)):
    rec = db[i]
    if email == rec['email']:
      firstNm = rec['fullNm'].split()[0]   #just first name
      body = firstNm + ' - thanks'
      try:
        sys.argv[2]
        srv = mailLib.create_service()
        msg = mailLib.create_message('aaron.boxer@gmail.com',email,'thanks',body)
        mailLib.send_message(srv,'me',msg)
        db[i]['lastGv'] = int(time.time())
        if 'gvCt' not in rec:
          db[i]['gvCt'] = 1
        else:
          db[i]['gvCt'] += 1
        if 'totAmt' not in rec:
          db[i]['totAmt'] = amt
        else:
          db[i]['totAmt'] += amt
      except:
        print(email,amt)

      break
  else:
    print('ERR - no email match')

mailLib.prStats(db)

outf = open(emailDb,'w') #rewrite the database
json.dump(db,outf)

