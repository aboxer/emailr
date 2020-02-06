import sys
import mailLib

ed = mailLib.emailDb('data/emailDb.csv')
ed.setDb(sys.argv[1])
ed.prStats()
ed.prTbl()
ed.exitDb()

