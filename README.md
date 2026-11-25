# Tirian Trains

Railway database covering routes, schedules, tickets, and train maintenance for CSCI41

---

## Group 15 - The Erds
### Members
- Michel Kristof Cabataña 
- Samantha Sofia Garcia
- Aldrin Joseph Nellas
- Nathaniel Joaquin Quijencio
- Hans Daniel Tan


--- 

## Startup

run the ff commands.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

default start is at http://127.0.0.1:8000


## Working file structure

```text
csci41-tirian-trains/
├── .gitignore                      
├── README.md                       
├── requirements.txt               
├── manage.py                       
├── tirian_trains/                   
│   ├── __init__.py                  
│   ├── settings.py                  # app registration and local SQLite settings
│   ├── urls.py                      # project routes, including Django admin
│   ├── asgi.py                      
│   └── wsgi.py                    
└── core/                            
    ├── __init__.py                  
    ├── apps.py                      # app configuration
    ├── models.py                    # where we put the railway models
    ├── admin.py                     # admin registration
    ├── views.py                     # for request handlers
    ├── tests.py                     # app tests
    └── migrations/                  # where the generated schema goes
        └── __init__.py              
```

## Proposed file structure

(tentative lang, we can omit some if not needed or change structure if you feel its easier)

```text
csci41-tirian-trains/
├── .gitignore                       
├── README.md                       
├── requirements.txt                 
├── manage.py                        
│
├── tirian_trains/                   # project-wide Django configuration
│   ├── __init__.py                  
│   ├── settings.py                  # configures apps, database, templates, and static files
│   ├── urls.py                      # cnnects railway, authentication, and admin routes
│   ├── asgi.py                      
│   └── wsgi.py                      
│
├── core/                            
│   ├── __init__.py                  
│   ├── apps.py                      
│   ├── models.py                    # defines railway tables, relationships, and constraints
│   ├── admin.py                     # configures staff management of records in Django admin
│   ├── views.py                     # handles schedule searches, ticket requests, and permissions
│   ├── tests.py                     # tests constraints, search, permissions, and ticket issuance
│   ├── forms.py                     # validates schedule filters and ticket form input
│   ├── urls.py                      # maps schedule and ticket URLs to views
│   ├── services.py                  # saves ticket, itinerary, and fares in one transaction
│   ├── migrations/                  
│   │   ├── __init__.py              
│   │   └── 0001_initial.py          # creates the initial railway tables and constraints
│   ├── management/                  # holds custom manage.py commands
│   │   ├── __init__.py           
│   │   └── commands/            
│   │       ├── __init__.py        
│   │       └── seed_data.py         # loads demo records and supports repeat runs
│   ├── templates/                   
│   │   └── core/                    
│   │       ├── schedule_list.html   # schedule search filters and results
│   │       ├── schedule_detail.html # trip times, stations, and train amenities
│   │       ├── ticket_form.html     # staff selects a passenger and confirms issuance
│   │       ├── ticket_list.html     # lists issued tickets
│   │       └── ticket_detail.html   # shows the receipt, itinerary, and stored fares
│   └── static/                      
│       └── core/                    
│           └── styles.css           
│
├── templates/                       # shared project templates
│   ├── base.html                    # common page layout and navigation
│   └── registration/                # template location used by Django auth views
│       └── login.html               # sign-in form
│
└── database/                        # SQL files
    ├── schema.sql                   # final PostgreSQL table
    ├── queries.sql                  # schedule, ticket, and maintenance queries
    └── verification.sql             # checks keys, demo records, and ticket totals
```
