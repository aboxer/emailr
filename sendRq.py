import mailLib

ed = mailLib.emailDb('data/emailDb.json')
gm = mailLib.gmailr(ed)

rqList = ed.getRqs()
gm.send_message(rqList)
ed.prStats()
ed.exitDb()
