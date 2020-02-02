import sys
import json
import mailLib

inf = open(sys.argv[1],'r')
db = []
for line in inf:
  rec = {}
  dat = line.split(',')
  rec['fullNm'] = dat[0].strip()
  rec['email'] = dat[1].strip()
  rec['grp'] = dat[2].strip()
  rec['rqCt'] = int(dat[3].strip())
  rec['lastRq'] = mailLib.str2ts(dat[4].strip())
  rec['totAmt'] = float(dat[5].strip())
  rec['lastGv'] = mailLib.str2ts(dat[6].strip())
  rec['gvCt'] = int(dat[7].strip())
  db.append(rec)

mailLib.prStats(db)
outf = open('data/emailDb.json','w')
json.dump(db,outf)

