# Emailer Tools Design

This is a bunch of programs to manage emails for my PMC ride. It consists of the following:

* setDb.py - add full records to database
* addGrp.py - add names and email address from a list to database group
* sendThx.py - send customized thank you email. NOTE: always run before sendRq.py
* sendRq.py - fetch names and emails from database and send customized request email
* rmRec.py - remove records if they have never given
* getStats.py - get various stats about database

## email data base structure
emailDb.json is a json list of the following structure.

[                     #email list containing email records of the following form
  {fullNm : string,   #first mid last
  email : string,     #email address
  grp : string,       #group of people used to select customizable message
  rqCt : int,         #number of requests made to this person
  lastRq : int,       #timestamp of last request
  totAmt: float,      #total amount given
  lastGv : int,       #timestamp of last give
  gvCt : int},        #number of times person has given
  .                   #another email record just like the one above
  .
  {}                  #last email record
]

##getStats.py

>python getStats.py > stats.txt

Output statistics from stats.json which has the following structure.
{lastThx: string, #last time sendThx.py was run
lastRq:string,    #last time sendRq was run
emailsSz: int,    #size of email list
giversCt: int,    #count of people who have donated
totAmt:float}     #total amount given

##addGrp.py

>python addGrp.py group newNms.txt > dbg.txt

put the group name in the text file name so you know what group you are adding to

Reads newNms.txt file of the following structure.
first mid last , email #middle name or initial is optional
.
.
.

If there is a database record matching that name and email it is a duplicate so ignore it. I don't want to send multiple different requests to the same person. Otherwise add a record to the emailDB.json, setting fullNm, email and grp. The other fields will be created by other tools 

groups I've identified so far 
tsg = torah study group
stl = shir tikva general
lhs = lawrence high school
msc = miscellaneous

##sendThx.py

>python sendThx.py thxEmails.txt > dbg.txt

Reads thxEmails.txt file of the following structure.
email - amount
.
.

Send the selected people the customized thanks for their group and update their gvCt and totAmt.

##sendRq.py

>python sendRq.py  [force] > dbg.txt

if force argument is excluded and there haven't been any donations since the last sendRq then exit. Run sendThx to update donation info. The run sendRq again. If there are no donations to update, run sendRq with the force argument.

Picks rqNum people from emailDb.json according to the following rules.
* Ignore anyone who has already donated.
* Ignore anyone who has received a request within specified days
* prioritize people with lowest rqCt

Send the selected people a customized request for their group and update their giveCt and lastRq.

##rmRec.py

>python rmvDb.py rmvNms.txt > dbg.txt

Reads rmvNms.txt file of the following structure.
email
.
.
.

If there is a database record matching that email, remove the whole record if they have never donated.

