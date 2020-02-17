#Create a complete Shir Tikvah email group that excludes special friends
import re
import tabulate
import random
import csv

#Create database of all emails to exclude from general List
exInfs = ['data/tsgGrp.csv','data/sjoGrp.csv','data/stfGrp.csv']
exDb = []
for exInf in exInfs:
  with open(exInf, newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    flag = False
    for row in spamreader:
      row = [x.strip(' ') for x in row] #strip white space from each element in row
      if flag == False: #skip first row
        cols = row
        flag = True
      else:
        rec = {}
        for col in cols:
          val = row.pop(0)
          rec[col] = val
        exDb.append(rec)

for row in exDb:
  print(row)

inf = open('data/shir_tikvah.txt','r')
lines = inf.readlines()
emailChk = re.compile('@')
emailCt = 0
exCt = 0
keepCt = 0
listSz = len(lines)
#shirDb = []
#shirList = [cols]
shirList = []
for i in range(listSz):
  line = lines[i].strip()
  if emailChk.search(line):
    emailCt += 1
    for j in range(i-1,i-4,-1): #look back a few lines for name
      back = lines[j]
      if re.match('Home:',back) or re.match('Mobile:',back):
        pass
      else:
        name = back.strip()
        break
    else:
      name = 'not found'
    for ex in exDb:  #skip anything in exclude list
      if ex['email'].lower() == line.lower() or ex['fullNm'].lower() == name.lower():
        exCt += 1
        print('exc',ex)
        break
    else:
      keepCt += 1
      shirList.append([name,line])
#      shirDb.append({'fullNm':name,'email':line})

random.shuffle(shirList) #shuffle so people in same family don't get email on same day -  NOTE:running this again gets differnt results
shirList.insert(0,cols)  #and put in header
tbl = tabulate.tabulate(shirList,headers = 'firstrow')
print(tbl)
print('emails = ',emailCt,'keeps = ',keepCt,'exList = ',len(exDb),'exCt = ',exCt)

with open('data/salGrp.csv', 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile)
  for row in shirList:
    spamwriter.writerow(row)

