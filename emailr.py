#!/Users/lawrenceboxer/Documents/projects/pmc/emailr/env/bin python
import sys
import re
import mailLib
import time
import msgMkr

#first parse the input arguments
upd_flag = False
dbg_flag = False
cmd = None
for i in range(1,len(sys.argv)):
  arg = sys.argv[i]
  if re.search('.csv$',arg): 
    fileNm = arg
    print('fileNm = ',arg)
  elif re.match('-',arg):
    opt = arg[1:] #chop of the dash
    if opt == 'dbg':
      dbg_flag = True
      print('upd = ','True')
    if opt == 'upd':
      upd_flag = True
      print('upd = ','True')
    elif re.match('tsg|stf|ind|sjo|try|fri',opt):
      grp = opt
  elif re.match('\+\d+',arg):
    sndCt = int(arg[1:]) #chop of the dash
    print('sndCt = ',sndCt)
  else:
    cmd = arg
    print('cmd = ',arg)


if dbg_flag == True:
  ed = mailLib.emailDb('data/emailDbg.csv','back/emailBbg','/Users/lawrenceboxer/Dropbox/emailDbg.csv') #create or open the db
else:
  ed = mailLib.emailDb('data/emailDb.csv','back/emailBk','/Users/lawrenceboxer/Dropbox/emailDb.csv') #create or open the db
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
    elif t[0] == 'sr': #create new message
      #body = msgMkr.mkMsg(rec['grp'] + '_rq1',rec)
      body = msgMkr.mkMsg('cus' + '_rq1',rec)
      msg = mailLib.create_message('aaron.boxer@gmail.com',rec['email'],' My Pan-Mass Challenge Ride for Alan Finder',body)
      print(body)
    elif t[0] == 'ch': #change column
      if t[1] == 'rqCt':
        try:
          rec['rqCt'] = int(t[2])
        except:
          rec['rqCt'] = None
          rec['lastRq'] = None
      elif t[1] == 'lastRq':
        try:
          rec['lastRq'] = mailLib.str2ts(t[2])
        except:
          rec['lastRq'] = int(time.time())
      elif t[1] == 'gvCt':
        try:
          rec['gvCt'] = int(t[2])
        except:
          rec['gvCt'] = None
          rec['lastGv'] = None
      elif t[1] == 'lastGv':
        try:
          rec['lastGv'] = mailLib.str2ts(t[2])
        except:
          rec['lastGv'] = int(time.time())
      elif t[1] == 'totAmt':
        try:
          rec['totAmt'] = float(t[2])
        except:
          rec['totAmt'] = None
      elif t[1] == 'act':
        try:
          if t[2].lower() == 'true':
            rec['act'] = True
          else:
            rec['act'] = False
        except:
          rec['act'] = False
      elif re.match('fullNm|email|grp|gvMeth',t[1]):
        try:
          rec[t[1]] = t[2]
        except:
          rec[t[1]] = None
      tbl = mailLib.db2Tbl([rec])
      print(tbl)
    elif t[0] == 'pt': #add record to database
      upd_flag = True
      if idx == None:
        ed.addRec(rec)
      elif idx < len(ed.db):
        ed.setRec(idx,rec)
        try:
          msg
          gm.send_message(True,[[idx,msg]])  #True = request, False = thanks
          del(msg)
        except:
          pass
        
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
  #ed.prStats()
  #ed.prTbl()
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
  sendList,msgList = ed.getRqs(grp,sndCt) #create a list of record indices and corresponding messages to send
  for snd in sendList:  #for debugging just print who gets the messages
    print(ed.getRec(snd))
  if upd_flag == True: #if update is set, send the messages. the gmailer will update the records if email is sent
    gm.send_message(True,msgList)  #True = request, False = thanks
else:
  print("""
bad command
""")

ed.prTbl()
ed.prStats()
if upd_flag == True:
  ed.exitDb()
