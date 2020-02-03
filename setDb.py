import sys
import mailLib

ed = mailLib.emailDb('data/emailDb.json')
ed.setDb(sys.argv[1])
ed.prStats()
ed.exitDb()

