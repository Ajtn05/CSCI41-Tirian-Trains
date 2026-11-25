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
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
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
│   ├── urls.py                      # connects railway, authentication, and admin routes
│   ├── asgi.py                      
│   └── wsgi.py                      
│
├── core/                            
│   ├── __init__.py                  
│   ├── apps.py                      
│   ├── models.py                    # defines railway tables, relationships, and constraints
│   ├── admin.py                     # configures staff management of records in Django admin
│   ├── views.py                     # handles railway pages, filters, and permissions
│   ├── tests.py                     # tests route rules, maintenance, scheduling, and ticket sales
│   ├── forms.py                     # validates schedule filters and ticket sales input
│   ├── urls.py                      # maps route, maintenance, schedule, and ticket pages
│   ├── services.py                  # saves a ticket and its trip fares in one transaction
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
│   │       ├── route_list.html      # lists local and inter-town routes
│   │       ├── route_detail.html    # shows stations, travel time, and fare
│   │       ├── train_list.html      # lists trains for maintenance review
│   │       ├── train_detail.html    # shows train specs and maintenance history
│   │       ├── schedule_list.html   # schedule search filters and results
│   │       ├── schedule_detail.html # trip times, stations, and assigned train
│   │       ├── ticket_form.html     # selects a passenger and one or more trips
│   │       ├── ticket_list.html     # lists issued tickets
│   │       └── ticket_detail.html   # shows the itinerary and stored fares in Lion coins
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
    ├── schema.sql                   # defines the PostgreSQL tables and constraints
    ├── queries.sql                  # route, schedule, ticket, and maintenance queries
    └── verification.sql             # checks keys, demo records, and ticket totals
```

## Rules from Deliverable 1

- Train maintenance shows train specs and history. Each train has at least one maintenance record and one scheduled trip. A maintenance record can list multiple crew members and tasks.
- Every station belongs to a route. Local routes share a fare and travel time. Each inter-town route connects two stations and uses the same fare and travel time in both directions.
- Each passenger has at least one ticket. A ticket belongs to one passenger, covers one or more trips, and totals their recorded fares in Lion coins.
- Each scheduled trip has one train and one route. Arrival time is departure time plus the route's travel time.
