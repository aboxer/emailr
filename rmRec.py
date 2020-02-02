import sys
import json
import mailLib

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

mailLib.prStats(db)

outf = open(emailDb,'w') #rewrite the database
json.dump(db,outf)
