import sys
#import json
import mailLib

ed = mailLib.emailDb('data/emailDb.json')
#ed.addDb(sys.argv[1],sys.argv[2])
ed.addGrp(sys.argv)
ed.prStats()
ed.exitDb()

