import sys
import json
import mailLib

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

mailLib.prStats(db)

outf = open(emailDb,'w') #rewrite the database
json.dump(db,outf)
