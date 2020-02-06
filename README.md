# Document Reader

## Folder Structure
```
├── README.md
├── int_docs           - useful documentation
│   └── design.md      - emailr design documentation
├── data
│   ├── emailDb.py     - database used by emailr
│   ├── tsgGrp.csv     - torah study group list
│   ├── addRecs.csv    - records to add to emaildDb
│   └── rmRecs.csv     - records to remove to emailDb

├── .gitignore
├── quickstart.py     - used by gmail API allow my gmail to be used by API
├── credentials.json  - used by gmail API for authentication
├── token.pickle      - used by gmail API during access to my gmail
├── msgMkr.py         - library of email messages
├── mailLib.py        - library of classes and routines
└──  emailr.py        - chooses email addresses from database and sends emails
```
## Local Setup
runs under python3

### Brief Description
A series of tools for managing emails for my pmc challange

### Prerequisites
I've only tested these tools in the following environment.
* Macbook Pro runnning OSX 10.15.2
* python 3.7

