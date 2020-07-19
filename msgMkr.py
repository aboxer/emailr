import re
from nameparser import HumanName


msgs = {
#first request to Torah Study Group
'tsg_rq1':
"""
Hi <firstNm>,

I'm beginning to raise funds for my Pan Mass Challenge ride in memory of Alan. I figured I'd start with the members of our Torah Study Group. We must have been very important to Alan because he attended as long as he could, even in obvious discomfort.

I have a webpage on the PMC website with some of my thoughts about Alan and some pictures of him , including one of us. You can click on this link, profile.pmc.org/AB0492 if you'd like to donate by credit card.

If you want to donate by check or Donor Advised Fund, here is the link on how to do it. https://www.pmc.org/ways-to-give

thanks, see you at Torah Study,
Aaron

PS: My address on this email is different from the one in the Shir Tikvah directory because I am using a different account to manage my PMC communications. I saw today that there has been some type of email scam sent to Shir Tikvah members in Rabbi Cari's name. If you are concerned about this email, let me know using my address in the Shir Tikvah directory under Lawrence Boxer (the usual one you have for me) or see me at Torah Study on Saturday.
""",
'sjo_rq1':
"""
Hi <firstNm>,

I'm beginning to raise funds for my Pan Mass Challenge ride in memory of Alan Finder. Like us, he made a musical contribution to Shir Tikvah through our chorus, Shir Chadash and Kiddush blessings on Friday nights. I know he is missed there.

I have a webpage on the PMC website with some of my thoughts about Alan and some pictures of him , including one of Alan singing with Sophia. You can click on this link, profile.pmc.org/AB0492 if you'd like to donate by credit card.

If you want to donate by check or Donor Advised Fund, here is the link on how to do it. https://www.pmc.org/ways-to-give. Please include my egift ID (AB0492) so I can get credit toward my fundraising commitment.

thanks, I'm looking forward to playing some music on Purim,
Aaron

PS: My address on this email is different from the one in the Shir Tikvah directory because I am using a different account to manage my PMC communications. I saw recently that there has been some type of email scam sent to Shir Tikvah members in Rabbi Cari's name. If you are concerned about this email, let me know using my address in the Shir Tikvah directory under Lawrence Boxer (Aaron is my middle name).
""",
'stf_rq1':
"""
Hi <firstNm>,

I was in the middle of raising funds for my Pan Mass Challenge ride in memory of Alan Finder when the coronavirus hit us, so I stopped. Since then the PMC has started an emergency response fund (see https://www.pmc.org/blog/emergency-response-fund) and I've started asking for donations again. You'll see from this link that PMC leadership understands that these are uncertain financial times for everyone and so do I. So anything you can give will be greatly appreciated.

Alan Finder was an integral part of the Shir Tikvah community for many years. He made a musical contribution to Shir Tikvah through our chorus, Shir Chadash and Kiddush blessings on Friday nights. I know he is missed there.

I have a webpage on the PMC website with some of my thoughts about Alan and some pictures. You can click on this link, profile.pmc.org/AB0492 if you'd like to donate by credit card.

If you want to donate by check or Donor Advised Fund, here is the link on how to do it. https://www.pmc.org/ways-to-give.  Please include my egift ID (AB0492) so I can get credit toward my fundraising commitment.


thanks for your support,
Aaron Boxer

PS: I saw recently that there has been some type of email scam sent to Shir Tikvah members in Rabbi Cari's name. If you are concerned about this email, contact me using my address in the Shir Tikvah directory under Lawrence Boxer (Aaron is my middle name).
""",
'tsg_thx':
"""
Hi <firstNm>,

I appreciate the support I'm getting from our Torah Study group. The last time I did something like this I was about 8 years old carrying one of those UNICEF cans on Halloween. I thought the coins were for me until my mom set me straight.

I hope you found the thoughts on my PMC webpage meaningful and I hope you enjoyed the pictures, epecially the one of us.

thanks, see you at Torah Study,
Aaron
""",
'gen_thx':
"""
Hi <firstNm>,

I appreciate your support.The last time I did something like this I was about 8 years old carrying one of those UNICEF cans on Halloween. I thought the coins were for me until my mom set me straight.

I hope you found the thoughts on my PMC webpage meaningful and I hope you enjoyed the pictures.

thanks again,
Aaron
""",
'lhs_rq1':
"""
Hi <firstNm>,

I hope this email finds you healthy and safe. So much has changed since our 50th LHS Reunion that I feel like it happened 50 years ago. 

Not long after the Reunion my good friend, Alan Finder, died of pancreatic cancer and I made plans to ride my bike in the Pan Mass Challenge to raise money for the Dana Farber Cancer Institute in his honor.

Alan Finder was an integral part of my religious community, Shir Tikvah in Winchester MA. We sang and prayed together at Friday Night Shabbat services and we studied Torah together on Saturday mornings. He is greatly missed by this whole community.

I have a webpage on the PMC website with some of my thoughts about Alan and some pictures. You can click on this link, profile.pmc.org/AB0492 if you'd like to donate by credit card.

If you want to donate by check or Donor Advised Fund, here is the link on how to do it. https://www.pmc.org/ways-to-give.  Please include my egift ID (AB0492) so I can get credit toward my fundraising commitment.

I understand that I am making this request during uncertain times for all of us and I will appreciate anything you feel you can give. 

thanks for your support,
Larry (Aaron) Boxer
""",
'cus_rq1':
"""
Hi <firstNm>,

I was in the middle of raising funds for my Pan Mass Challenge ride in memory of Alan Finder when the coronavirus hit us, so I stopped. Since then the PMC has started an emergency response fund (see https://www.pmc.org/blog/emergency-response-fund) and I've started asking for donations again. You'll see from this link that PMC leadership understands that these are uncertain financial times for everyone and so do I. Anything you can give will be greatly appreciated.

Alan Finder was an integral part of the Shir Tikvah community for many years. He made a musical contribution to Shir Tikvah through our chorus, Shir Chadash and Kiddush blessings on Friday nights. I know he is missed there.

I have a webpage on the PMC website with some of my thoughts about Alan and some pictures. You can click on this link, profile.pmc.org/AB0492 if you'd like to donate by credit card.

If you want to donate by check or Donor Advised Fund, here is the link on how to do it. https://www.pmc.org/ways-to-give.  Please include my egift ID (AB0492) so I can get credit toward my fundraising commitment.


thanks for your support,
Aaron Boxer

PS: I saw recently that there has been some type of email scam sent to Shir Tikvah members in Rabbi Cari's name. If you are concerned about this email, contact me using my address in the Shir Tikvah directory under Lawrence Boxer (Aaron is my middle name).
"""
}

def mkMsg(msgId,rec):
  #if rq == True:
  #  msgId = rec['grp'] + '_rq1'
  #else:
  #  msgId = rec['grp'] + '_thx'
  msg = msgs[msgId]

  #find all the replaceble fields in the message
  rpllocs = []
  rpls = re.finditer('<\w+>',msg,re.IGNORECASE)
  for rpl in rpls:
    rpllocs.append(rpl.span()) #span[0] = < and span[1] = char after >

  #replace them with data from rec
  newMsg = ''
  newPtr = 0
  for rplloc in rpllocs:
    beg = rplloc[0]
    end = rplloc[1]
    newMsg = newMsg + msg[newPtr:beg]
    rpl = msg[beg:end]
    fieldNm = msg[beg+1:end-1] #chop off < and >
    if fieldNm == 'firstNm':
      name = HumanName(rec['fullNm'])
      #msg = msg.replace(rpl,name.first)
      newMsg = newMsg + name.first
      newPtr = end
    if fieldNm == 'fileMsg':
      mfile = open('fileMsg.txt','r')
      cus = mfile.read()
      mfile.close()
      #msg = msg.replace(rpl,cus)
      newMsg = newMsg + cus

  #return msg
  newMsg = newMsg + msg[end:]
  return newMsg
 
