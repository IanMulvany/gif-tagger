
# Project idea
Create a local replacement for YNAB.

I mainly just use YNAB for tagging my transactions, and looking at historical reports. I've decided to try to use elasticsearch and kibabna for reporting historical data, and this repo will be used for tagging transactions downloaded in the qif format from my bank, and then adding those tagged transactions into an elasticsearch instance.  

# Status
In development, not at all even near to functioning. 

# Main use case
Upload a QIF file, and make it easy to tag transactions. Push tagged file into
an elastic search instance. Use the es instance to do reporting.

# Secondary use case
Create a budget overview against categories. Show how spend is going vs budget.

# Key features
- upload a qif file
- parse the qif file
- display entries from the qif file
- provide a way to tag the entries from the qif file
- make tagging be do-able using the keyboard only
- upload the result to es

# Secondary features
- implement keyboard shortcuts to make tagging easier
- auto tag an entry based on payee, and history of what we tagged that payee before  
- display all payments by tab, by payee from es

# App resources

http://flask.pocoo.org/docs/0.11/blueprints/#blueprints
http://flask.pocoo.org/docs/0.11/patterns/packages/
