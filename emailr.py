import sys
import re
import mailLib

#first parse the input arguments
upd_flag = False
cmd = None
for i in range(1,len(sys.argv)):
  arg = sys.argv[i]
  if re.search('.csv$',arg): 
    fileNm = arg
    print('fileNm = ',arg)
  elif re.match('-',arg):
    opt = arg[1:] #chop of the dash
    if opt == 'upd':
      upd_flag = True
      print('upd = ','True')
    elif re.match('\d+',opt):
      sndCt = opt
      print('sndCt = ',opt)
    else:
      grp = opt
  else:
    cmd = arg
    print('cmd = ',arg)


ed = mailLib.emailDb('data/emailDb.csv') #create or open the db
gm = mailLib.gmailr(ed)
if cmd == 'mr':
  ed.prStats()
  ed.prTbl()
  upd_flag = False #don't overwrite database just to get a report
elif cmd == 'ag':
  ed.addGrp(grp,fileNm)
elif cmd == 'ld':
  ed.setDb(fileNm)
elif cmd == 'ch':
  ed.chgDb(fileNm)
elif cmd == 'rr':
  ed.rmRec(fileNm)
elif cmd == 'sr':
  sendList,msgList = ed.getRqs()
  for snd in sendList:
    print(ed.getRec(snd))
  if upd_flag == True:
    gm.send_message(msgList)
else:
  print("""
bad command
""")

ed.prStats()
ed.prTbl()
if upd_flag == True:
  ed.exitDb()
