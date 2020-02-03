import mailLib

ed = mailLib.emailDb('data/emailDb.json')
gm = mailLib.gmailr()

rqList = ed.getRqs()
dnList = gm.send_message(rqList)
ed.updRqs(dnList)
ed.prStats()
ed.exitDb()
