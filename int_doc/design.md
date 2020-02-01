# Emailer Tools Design

This is a bunch of programs to manage emails for my PMC ride. It consists of the following:

* addDb.py - add names and email address from a list to database
* sendThx.py - send customized thank you email. NOTE: always run before sendRq.py
* sendRq.py - fetch names and emails from database and send customized request email
* rmvDb.py - remove names and email address from a list to database
* getStats.py - get various stats about database

## email data base structure
emailDb.json is a json list of the following structure.

[                     #email list containing email records of the following form
  {fullNm : string,   #first mid last
  email : string,     #email address
  grp : string,       #group of people used to select customizable message
  rqCt : int,         #number of requests made to this person
  lastRq : string,    #date of last request
  totAmt: float,      #total amount given
  lastGv : string,    #date of last give
  gvCt : int},        #number of times person has been thanked
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

##addDb.py

>python addDb.py newNms.txt > dbg.txt

Reads newNms.txt file of the following structure.
grp                    #used to decide which customized email to send
first mid last - email
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

Send the selected people the customized thanks for their group and update their thxCt and totAmt.

##sendRq.py

>python sendRq.py rqNum days > dbg.txt

NOTE: checks that stats database to see if sendThx.py has been run after the previous sendTq.py

Picks rqNum people from emailDb.json according to the following rules.
* Ignore anyone who has already donated.
* Ignore anyone who has received a request within specified days
* prioritize people with lowest rqCt

Send the selected people a customized request for their group and update their giveCt and lastRq.

##rmvDb.py

>python rmvDb.py rmvNms.txt > dbg.txt

Reads rmvNms.txt file of the following structure.
email
.
.
.

If there is a database record matching that email, remove the whole record.
