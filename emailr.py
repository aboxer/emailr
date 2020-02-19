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


ed = mailLib.emailDb('data/emailDb.csv','data/emailBk','/Users/lawrenceboxer/Dropbox/emailDb.csv') #create or open the db
gm = mailLib.gmailr(ed)
if cmd == None:   #interactive mode
  intFlag = True
  while intFlag:
    t = input('> ').split(' ')
    if t[0] == 'qt':  #quit
      intFlag = False
    elif t[0] == 'gn': #get record by name
      idxs = ed.getNm(t[1])
      recDb = []
      for ix in idxs:
        recDb.append(ed.getRec(ix))
      rec = recDb[0]  #pick the top score
      idx = idxs[0]
      tbl = mailLib.db2Tbl(recDb)
      print(tbl)
    elif t[0] == 'ge': #get record by email
      idx = ed.getEmail(t[1])
      if idx != None:
        rec = ed.getRec(idx)
        tbl = mailLib.db2Tbl([rec])
        print(tbl)
    elif t[0] == 'cr': #create new record
      idx = None
      rec = ed.emptyRec()
      rec['fullNm'] = ' '.join(t[1:])
      rec['act'] = True
      tbl = mailLib.db2Tbl([rec])
      print(tbl)
    elif t[0] == 'ch': #change column
      if t[1] == 'rqCt':
        rec['rqCt'] = int(t[2])
      elif t[1] == 'lastRq':
        rec['lastRq'] = mailLib.str2ts(t[2])
      elif t[1] == 'gvCt':
        rec['gvCt'] = int(t[2])
      elif t[1] == 'lastGv':
        rec['lastGv'] = mailLib.str2ts(t[2])
      elif t[1] == 'totAmt':
        rec['totAmt'] = float(t[2])
      elif t[1] == 'act':
        if t[2].lower() == 'true':
          rec['act'] = True
        else:
          rec['act'] = False
      else:
        rec[t[1]] = t[2]
      tbl = mailLib.db2Tbl([rec])
      print(tbl)
    elif t[0] == 'pt': #add record to database
      upd_flag = True
      if idx == None:
        ed.addRec(rec)
      else:
        ed.setRec(idx,rec)
    elif t[0] == 'rr': #remove record from database
      upd_flag = True
      if idx != None:
        ed.rmvRec(idx)
      print('dbg0',upd_flag,idx)

    elif t[0] == 'at': #add to total
      amt = float(t[1])
      if rec['gvCt'] == None: #first time
        rec['totAmt'] = amt
      else:
        rec['totAmt'] += amt
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
