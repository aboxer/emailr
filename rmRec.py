import sys
#import json
import mailLib

ed = mailLib.emailDb('data/emailDb.csv')
ed.rmRec(sys.argv)
ed.prStats()
ed.prTbl()
ed.exitDb()

