#!/Users/lawrenceboxer/Documents/projects/pmc/emailr/env/bin python
import sys
import re
import mailLib
import time

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


ed = mailLib.emailDb('data/emailDb.csv','data/emailBk.csv','/Users/lawrenceboxer/Dropbox/emailDb.csv') #create or open the db
gm = mailLib.gmailr(ed)
if cmd == None:   #interactive mode
  intFlag = True
  while intFlag:
    t = input('> ').split(' ')
    if t[0] == 'qt':  #quit
      intFlag = False
    elif t[0] == 'ge': #get record by email
      idx = ed.getEmail(t[1])
      if idx != None:
        rec = ed.getRec(idx)
        tbl = mailLib.db2Tbl([rec])
        print(tbl)
    elif t[0] == 'cam': #change amount given
      amt = float(t[1])
      if rec['gvCt'] == None: #first time
        rec['totAmt'] = amt
        rec['gvMeth'] = 'online' #most will be online so default to this
      else:
        rec['totAmt'] += amt
      tbl = mailLib.db2Tbl([rec])
      print(tbl)
    elif t[0] == 'cme': #change give method
      rec['gvMeth'] = t[1]
      tbl = mailLib.db2Tbl([rec])
      print(tbl)
    elif t[0] == 'thx': #send thank you
      msg = ed.getThx(idx) #create a thank you message
      gm.send_message(False,[[idx,msg]])  #True = request, False = thanks
      upd_flag = True
      
elif cmd == 'mr':
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
  sendList,msgList = ed.getRqs() #create a list of record indices and corresponding messages to send
  for snd in sendList:  #for debugging just print who gets the messages
    print(ed.getRec(snd))
  if upd_flag == True: #if update is set, send the messages. the gmailer will update the records if email is sent
    gm.send_message(True,msgList)  #True = request, False = thanks
else:
  print("""
bad command
""")

ed.prStats()
ed.prTbl()
if upd_flag == True:
  ed.exitDb()
