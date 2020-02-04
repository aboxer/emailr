import re

msgs = {
#first request to Torah Study Group
'tsg_rq1':
"""
Hi <firstNm>,

I'm beginning to raise funds for my Pan Mass Challenge ride in memory of Alan. I figured I'd start with the members of our Torah Study Group. We must have been very important to Alan because he attended as long as he could, even in obvious discomfort.

I have a webpage on the PMC website with some of my thoughts about Alan and some pictures of him , including one of us. You can click on this link, profile.pmc.org/AB0492 if you'd like to donate by credit card.

thanks, see you at Torah Study,
Aaron
"""
}

def mkMsg(msgId,rec):
  msg = msgs[msgId]

  #find all the replaceble fields in the message
  rpllocs = []
  rpls = re.finditer('<\w+>',msg,re.IGNORECASE)
  for rpl in rpls:
    rpllocs.append(rpl.span()) #span[0] = < and span[1] = char after >

  #replace them with data from rec
  for rplloc in rpllocs:
    beg = rplloc[0]
    end = rplloc[1]
    rpl = msg[beg:end]
    fieldNm = msg[beg+1:end-1] #chop off < and >
    if fieldNm == 'firstNm':
      firstNm = rec['fullNm'].split()[0]   #just first name
      msg = msg.replace(rpl,firstNm)

  return msg
 
