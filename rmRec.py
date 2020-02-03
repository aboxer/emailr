import sys
#import json
import mailLib

ed = mailLib.emailDb('data/emailDb.json')
ed.rmRec(sys.argv)
ed.prStats()
ed.exitDb()

