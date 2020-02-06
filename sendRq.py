import mailLib

ed = mailLib.emailDb('data/emailDb.csv')
gm = mailLib.gmailr(ed)

rqList = ed.getRqs()
gm.send_message(rqList)
ed.prStats()
ed.prTbl()
ed.exitDb()
