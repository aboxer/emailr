#Emailer Tools Design

This is a program to manage emails for my PMC ride. It has a command line of the following form.

>python emailr cmd -options filenames

It has the following commands.

* ag - add a group of names and email address from a list to database group
* sr - fetch names and emails from database and send customized request email
* st - send customized thank you email. NOTE: always run before sendRq.py
* rg - remove records if they have never given money
* mr - make report

A help message is displayed if the command is not recognized or omitted.

##email data base structure
emailDb.csv is a csv file. The required first row is the header with the following keywords. There is a row for each person in the same order as the hearer

keyword  description
-------------------------------------------------------------------------------------
fullNm   #the first word is considered the first name. Any number of wrods is allowed
email    #email address
grp      #group of people used to select customizable message
rqCt     #integer of requests made to this person
lastRq   #mm/dd/yyyy of last request
amt      #float of total amount given
lastGv   #mm/dd/yyyy of last donation
gvCt     #integer of times person has given
act      #true = requests allowed, false = requests not allowed

##Add Group - ag
>python emailr.py ag -group newNms.csv > dbg.txt

Reads newNms.csv file with the following first row header and adds all the people in it to the same group

keyword  description
-------------------------------------------------------------------------------------
fullNm   #the first word is considered the first name. Any number of wrods is allowed
email    #email address

If there is a database record matching that name and email it is a duplicate so ignore it. I don't want to send multiple different requests to the same person. Otherwise add a record to the emailDB.json, setting fullNm, email, grp and act=True. The other fields will be created by other tools 

groups I've identified so far 
* tsg = torah study group
* stl = shir tikva general
* lhs = lawrence high school
* msc = miscellaneous

TIP: put the group name in the text file name so you know what group you are adding to

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
amt      #float of amount given


##Remove Group - rg
>python emailr.py rg rmGrp.csv > dbg.txt

If there is a database record matching that email, remove the whole record if they have never donated.
The emailr gives you a prompt asking asking if you want to continue.

Reads rmGrp.csv file with the following first row header.

keyword  description
-------------------------------------------------------------------------------------
email    #email address

##Meke Report - mr
>python emailr.py mk anyDb.csv > dbg.txt

Does comparison of any  database file to emailDB and outputs a report to stdout
