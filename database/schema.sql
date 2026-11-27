CREATE TABLE Passenger(
    Passenger_ID INT NOT NULL PRIMARY KEY, 
    Last_Name VARCHAR(50) NOT NULL,
    Given_Name VARCHAR(50) NOT NULL, 
    Middle_Initial VARCHAR(2) NOT NULL, 
    Birth_Date DATE NOT NULL, 
    Gender VARCHAR(50) NOT NULL, 
    CHECK (Passenger_ID > 0), 
    CHECK (Middle_Initial SIMILAR TO '[A-Z]\.'),
    CHECK (Birth_Date <= CURRENT_DATE),
    CHECK (Gender IN ('Male', 'Female', 'Other', 'Prefer Not to Say'))
); 

CREATE TABLE Station( 
    Station_ID INT NOT NULL PRIMARY KEY, 
    Name VARCHAR(100) NOT NULL, 
    CHECK (Station_ID > 0)
);

CREATE TABLE Route(
    Route_ID INT NOT NULL PRIMARY KEY, 
    Travel_Time INT NOT NULL, 
    Cost INT NOT NULL, 
    Type VARCHAR(20) NOT NULL, 
    CHECK (Route_ID > 0), 
    CHECK (Travel_Time > 0), 
    CHECK (Cost > 0), 
    CHECK (Type IN ('local', 'inter-town'))
);

CREATE TABLE Train(
    Train_ID INT NOT NULL PRIMARY KEY, 
    Max_Speed INT NOT NULL, 
    Number_of_Seats INT NOT NULL, 
    Number_of_Toilets INT NOT NULL DEFAULT 0, 
    Reclining_Seats BOOLEAN NOT NULL DEFAULT FALSE, 
    Folding_Tables BOOLEAN NOT NULL DEFAULT FALSE, 
    Disability_Access BOOLEAN NOT NULL DEFAULT FALSE, 
    Luggage_Storage BOOLEAN NOT NULL DEFAULT FALSE,
    Vending_Machines BOOLEAN NOT NULL DEFAULT FALSE, 
    Food_Service BOOLEAN NOT NULL DEFAULT FALSE, 
    Type CHAR(1) NOT NULL, 
    CHECK (Train_ID > 0), 
    CHECK (Max_Speed > 0), 
    CHECK (Number_of_Seats >=0),
    CHECK (Number_of_Toilets >=0), 
    CHECK (Type IN ('A', 'S'))
);

CREATE TABLE Crew_In_Charge(
    Crew_ID INT NOT NULL PRIMARY KEY, 
    First_Name_Initial VARCHAR(2) NOT NULL, 
    Last_Name VARCHAR(50) NOT NULL, 
    CHECK (Crew_ID > 0), 
    CHECK (First_Name_Initial SIMILAR TO '[A-Z]\.')
);

CREATE TABLE Local_Route(
    Local_Route_ID INT NOT NULL PRIMARY KEY, 
    Start_Station_ID INT NOT NULL, 
    End_Station_ID INT NOT NULL, 
    FOREIGN KEY (Local_Route_ID) REFERENCES Route(Route_ID), 
    FOREIGN KEY (Start_Station_ID) REFERENCES Station(Station_ID), 
    FOREIGN KEY (End_Station_ID) REFERENCES Station(Station_ID), 
    CHECK (Start_Station_ID != End_Station_ID)
);

CREATE TABLE Inter_Town_Route(
    Inter_Town_Route_ID INT NOT NULL PRIMARY KEY, 
    FOREIGN KEY (Inter_Town_Route_ID) REFERENCES Route(Route_ID)
);

CREATE TABLE Travel_Details(
    Route_ID INT NOT NULL PRIMARY KEY, 
    Origin INT NOT NULL, 
    Destination INT NOT NULL, 
    FOREIGN KEY (Route_ID) REFERENCES Route(Route_ID),
    FOREIGN KEY (Origin) REFERENCES Station(Station_ID),
    FOREIGN KEY (Destination) REFERENCES Station(Station_ID),
    CHECK (Origin != Destination)
);

CREATE TABLE Ticket( 
    Ticket_ID INT NOT NULL PRIMARY KEY, 
    Purchase_Date DATE NOT NULL, 
    Total_Cost INT NOT NULL DEFAULT 0, 
    Passenger_ID INT NOT NULL, 
    CHECK (Ticket_ID > 0),
    CHECK (Total_Cost >= 0), 
    CHECK (Purchase_Date <= CURRENT_DATE),
    FOREIGN KEY (Passenger_ID) REFERENCES Passenger(Passenger_ID)
);

CREATE TABLE Maintenance_History(
    Maintenance_ID INT NOT NULL PRIMARY KEY, 
    Train_ID INT NOT NULL, 
    Crew_ID INT NOT NULL, 
    Date DATE NOT NULL, 
    Tasks VARCHAR(255) NOT NULL,  
    Condition VARCHAR(255) NOT NULL, 
    CHECK (Condition IN ('Excellent', 'Very Good', 'Good', 'Satisfactory', 'Fair', 'Poor', 'Very Poor')), 
    CHECK (Date <= CURRENT_DATE), 
    FOREIGN KEY (Train_ID) REFERENCES Train(Train_ID), 
    FOREIGN KEY (Crew_ID) REFERENCES Crew_In_Charge(Crew_ID)
);

CREATE TABLE Inter_Town_Route_Station(
    PRIMARY KEY (Inter_Town_Route_ID, Station_Slot), 
    Inter_Town_Route_ID INT NOT NULL, 
    Station_Slot INT NOT NULL CONSTRAINT Max2 CHECK (Station_Slot BETWEEN 0 AND 1),
    Station_ID INT NOT NULL, 
    UNIQUE (Inter_Town_Route_ID, Station_ID), 
    FOREIGN KEY (Inter_Town_Route_ID) REFERENCES Inter_Town_Route(Inter_Town_Route_ID), 
    FOREIGN KEY (Station_ID) REFERENCES Station(Station_ID)
);

CREATE TABLE Trip_Schedule(
    Trip_Schedule_ID INT NOT NULL PRIMARY KEY, 
    Date DATE NOT NULL, 
    Departure_Time TIME NOT NULL, 
    Arrival_Time TIME NOT NULL, 
    Route_ID INT NOT NULL, 
    Train_ID INT NOT NULL, 
    CHECK(Trip_Schedule_ID > 0), 
    FOREIGN KEY (Route_ID) REFERENCES Route(Route_ID), 
    FOREIGN KEY (Train_ID) REFERENCES Train(Train_ID)
);

CREATE TABLE A_Series(
    A_Train_ID INT NOT NULL PRIMARY KEY, 
    Model VARCHAR(50) NOT NULL, 
    A_Route_ID INT NOT NULL, 
    FOREIGN KEY (A_Train_ID) REFERENCES Train(Train_ID), 
    FOREIGN KEY (A_Route_ID) REFERENCES Inter_Town_Route(Inter_Town_Route_ID),
    CHECK (Model SIMILAR TO 'A-[1-9][0-9]*')
);

CREATE TABLE S_Series(
    S_Train_ID INT NOT NULL PRIMARY KEY, 
    Model VARCHAR(50) NOT NULL, 
    S_Route_ID INT NOT NULL, 
    FOREIGN KEY (S_Train_ID) REFERENCES Train(Train_ID), 
    FOREIGN KEY (S_Route_ID) REFERENCES Local_Route(Local_Route_ID),
    CHECK (Model SIMILAR TO 'S-[1-9][0-9]*')
);

CREATE TABLE Trip_Itinerary(
    PRIMARY KEY (Ticket_ID, Trip_Schedule_ID), 
    Ticket_ID INT NOT NULL, 
    Trip_Schedule_ID INT NOT NULL, 
    Historical_Cost INT NOT NULL DEFAULT 0, 
    CHECK (Historical_Cost >= 0), 
    FOREIGN KEY (Ticket_ID) REFERENCES Ticket(Ticket_ID),
    FOREIGN KEY (Trip_Schedule_ID) REFERENCES Trip_Schedule(Trip_Schedule_ID)
);
