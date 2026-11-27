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

Use Python 3.12 or newer. Run these commands from the repo root.

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py seed_data
python3 manage.py createsuperuser
python3 manage.py runserver
```

Open http://127.0.0.1:8000/ and use **Sign in** with the account you created. Staff can inspect sample trains, routes, and trips under **Admin**. The seed command adds one local link, two connecting inter-town trips, train maintenance records, and a two-trip ticket totaling 26 Lion coins. Run it on a development database. Rerunning it reuses the sample records and their original dates.

### PostgreSQL setup

The default database is local SQLite. With PostgreSQL running, create a database and set `PGDATABASE` before applying migrations.

```sh
export PGDATABASE=tirian_trains
createdb "$PGDATABASE"
python3 manage.py migrate
python3 manage.py seed_data
```

Set `PGUSER`, `PGPASSWORD`, `PGHOST`, and `PGPORT` if your local connection requires them. Use a fresh database for the app's migrations. The draft in `database/schema.sql` can be run separately against an empty PostgreSQL database.

### Starting feature work

- Add feature URLs in `core/urls.py` and views in `core/views.py`. App templates go in `core/templates/core/` and extend `base.html`. Use the named `login` URL for views that require sign-in.
- The initial models map the current draft SQL. Supply an explicit ID when creating a railway record with its own integer primary key. The draft allows up to two numbered station slots per inter-town route and has one crew member and task text field per maintenance record.
- Run `python3 manage.py check` and `python3 manage.py makemigrations --check --dry-run` before merging.


## Working file structure

```text
csci41-tirian-trains/
├── .gitignore                      
├── README.md                       
├── requirements.txt               
├── manage.py                       
├── database/
│   └── schema.sql                   # supplied PostgreSQL draft
├── templates/
│   ├── base.html                    # shared layout
│   └── registration/
│       └── login.html               # sign-in form
├── tirian_trains/                   
│   ├── __init__.py                  
│   ├── settings.py                  # app registration and database settings
│   ├── urls.py                      # project routes, sign-in, and admin
│   ├── asgi.py                      
│   └── wsgi.py                    
└── core/                            
    ├── __init__.py                  
    ├── apps.py                      # app configuration
    ├── models.py                    # models for the 15 draft railway tables
    ├── validators.py                # validates dates, initials, and train model codes
    ├── admin.py                     # admin registration
    ├── views.py                     # for request handlers
    ├── urls.py                      # app routes
    ├── tests.py                     # placeholder for app tests
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py          # creates the draft railway tables
    ├── management/commands/
    │   └── seed_data.py             # adds sample railway records
    └── templates/core/
        └── home.html                # app landing page
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
│   ├── validators.py                # validates dates, initials, and train model codes
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
