#Emailer Tools Design

This is a program to manage emails for my PMC ride. It has a command line of the following form.

>python emailr cmd -options filenames

It has the following commands.

* ld - load some new records
* ag - add a group of names and email address from a list to database group
* ch - change fields in existing records
* rr - remove records if they have never given money
* sr - fetch names and emails from database and send customized request email
* st - send customized thank you email. NOTE: always run before sendRq.py
* mr - make report

A help message is displayed if the command is not recognized or omitted.

Running emailr with no emailDb.csv will create a blank one, even if there is no valid command

##email data base structure
emailDb.csv is a csv file. The required first row is the header with the following keywords. There is a row for each person in the same order as the hearer

keyword  description                                                        default
------------------------------------------------------------------------------------------------------
fullNm   #the first word is considered the first name.                      None
email    #email address                                                     required
grp      #group of people used to select customizable message               None
rqCt     #integer of requests made to this person                           0
lastRq   #mm/dd/yyyy of last request                                        None
gvCt     #integer of times person has given                                 0
lastGv   #mm/dd/yyyy of last donation                                       None
totAmt   #float of total amount given                                       0.0
act      #true = requests allowed, false = requests not allowed             True

##Load Records - ld
>python emailr.py ld  ldNms.csv > dbg.txt

Reads ldNms.csv file and adds the records to the database. email column MUST be included. Any missing columns are set to the default.

##Add Group - ag
>python emailr.py ag -group newNms.csv > dbg.txt

Reads newNms.csv file and adds the records to the database. email column MUST be included. grp column will be ignored if included and grp will be set to -group. Any missing columns are set to the default.

If there is a database record matching that email it is a duplicate so ignore it. I don't want to send multiple different requests to the same person.

groups I've identified so far 
* tsg = torah study group
* stl = shir tikva general
* lhs = lawrence high school
* msc = miscellaneous

TIP: put the group name in the text file name so you know what group you are adding to

##Change Records - ch
>python emailr.py ch  chNms.csv > dbg.txt

Reads chNms.csv file and change existing records to the database. email column MUST be included and cannot be changed.

##Remove Records - rr
>python emailr.py rr  rmNms.csv > dbg.txt

Reads rmNms.csv file and remove the records to the database. email column MUST be included. All others will be ignored.

Records for people who have donated money cannot be removed. They can be set inactive so they get no more emails

TIP: if you REALLY must remove a person who has donated money, First change gvCt to zero and then remove it

##Send Request - sr
>python emailr.py sr -s -num > dbg.txt

The list of database entries that changes is sent to stdout.
The actual emails wont be sent if -s is omitted
The number of emails sent is specified by -num

If lastRq for the whole database is later than lastGv the email gives you a prompt asking asking if you want to continue.

>No donations since last request. Continue Y/n? :

Picks num people from emailDb.csv according to the following rules.
* pick only people who have not donated
* Ignore anyone who has received a request within 14 days
* prioritize people with lowest rqCt

Send the selected people a customized request for their group and update their rqCt and lastRq. There are three customizable messages for each group. They are the following

* first request
* nth request
* last request 

##Send Thanks - st
>python emailr.py st -s thxGrp.csv > dbg.txt

Send a customized thank you to everyone on the list. Ignore entries where the lastGv date is the same or earlier than the one already in the database. Update amt, gvCt and lastGv with the current time. Unmatchable emails are ignored but are sent to stdout.

The list of database entries that changes is sent to stdout.
The actual emails wont be sent if -s is omitted

Reads thxGrp.csv file with the following first row header.

keyword  description
-------------------------------------------------------------------------------------
email    #email address
lastGv   #date of donation
totAmt   #float of amount given

##Meke Report - mr
>python emailr.py mk anyDb.csv > dbg.txt

Does comparison of any  database file to emailDB and outputs a report to stdout
