#import json
import mailLib

ed = mailLib.emailDb('data/emailDb.csv')
ed.prStats()
ed.prTbl()
ed.exitDb()
