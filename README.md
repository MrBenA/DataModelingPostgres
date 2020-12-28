# SparkifyDB

## Project overview
Sparkify offers a music streaming service through desktop and hand-held devices.<br>
To enable Sparkify to analyse data collected though their music streaming applications, Sparkify wish to establish
a relational analytical database to gain insight from the songs played by their user-base.



### Repository

#### Files to run project...
- [ *data* ] Directory structure with song and log file data, as JSON format.
- [ *create_tables.py* ] (Python 3 script): Creates sparkify database and necessary database tables.
- [ *etl.py* ] (Python 3 script): Main data processing script; Song and log file Extract, Transform and Load functions.
- [ *sql_queries.py* ] (Python 3 script): Table creation and insert SQL statements used by etl.py
  
#### Development / Testing...
- [ *etl.ipynb* ] (Jupyter notebook): ETL development
- [ *test.ipynb* ] (Jupyter notebook): Database querying statements after ETL



### Running the project
(*ensure a local PostgreSQL database server is running and configured with the following default database;<br>
dbname=studentdb, user=student, password=student*)
1. Download project data and Python scripts, as listed above, to a local directory.
2. Open your system CLI and change directory to where the project files are saved.<br>
   
        C:\users\username>cd C:\users\username\path\to\project
   
3. Run first Python script to create the sparkify database and table schema... *create_tables.py*;<br>

        C:\users\username>cd C:\users\username\path\to\project>python3 create_tables.py

4. Run second python script to process the JSON files and populate database tables... *etl.py*;<br>

        C:\users\username>cd C:\users\username\path\to\project>python3 etl.py 

---
## Dataset
2No. datasets are available for ingest to the Sparkify analytical database, which are required to carry out relevant<br>
song play analysis.

### Song data
Song data resides in JSON format, with each file containing metadata about a specific song, and the song's artist.<br>
Within Sparkify's file storage, song files are partitioned by the first three letters of each song's track ID.

Filepath example...

    song_data/A/B/C/TRABCEI128F424C983.json
    song_data/A/A/B/TRAABJL12903CDCF1A.json

TRAABJL12903CDCF1A.json song file content...

    {
    "num_songs": 1,
    "artist_id": "ARJIE2Y1187B994AB7",
    "artist_latitude": null,
    "artist_longitude": null,
    "artist_location": "",
    "artist_name": "Line Renaud",
    "song_id": "SOUPIRU12A6D4FA1E1",
    "title": "Der Kleine Dompfaff",
    "duration": 152.92036,
    "year": 0
    }

###  Log data
User activity logs, collected via the Sparkify music streaming applications, also resides in JSON format.<br>
Each file represents a single day and contains information about each user and their session details for that day.
Within Sparkify's file storage, log files are partitioned by the month and year.

    log_data/2018/11/2018-11-12-events.json
    log_data/2018/11/2018-11-13-events.json

2018-11-12-events.json log file content...

    {
    "artist":null,
    "auth":"Logged In",
    "firstName":"Celeste",
    "gender":"F",
    "itemInSession":0,
    "lastName":"Williams",
    "length":null,
    "level":"free",
    "location":"Klamath Falls, OR",
    "method":"GET",
    "page":"Home",
    "registration":1541077528796.0,
    "sessionId":438,
    "song":null,
    "status":200,
    "ts":1541990217796,
    "userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64)<br>
                AppleWebKit\/537.36 (KHTML, like Gecko)<br>
                Chrome\/37.0.2062.103 Safari\/537.36\"",
    "userId":"53"
    }

---

## Database Overview
The proposed analytical database shall be optimised for song play analysis and shall be structured around a snowflake<br>
schema design, consisting of a fact and various dimension tables.

### Table summary

**Table Name**  | **Description**
--------------- | ---------------
**songplays** | Fact Table;  Log data associated with song plays
**users** | Dimension Table; Registered application users
**songs** | Dimension Table; Songs in music database
**artists** | Dimension Table; Artists in music database
**time** | Dimension Table; Timestamps of **songplays** records, broken down into specific units

## Table Schema and samples

### Table: songplays

**Column name** | **Data type** | **Column description**
----------- | --------- | ------------------
**songplay_id**  | SERIAL | PRIMARY KEY
**start_time** | TIMESTAMP | NOT NULL
**user_id** | VARCHAR | NOT NULL
**level** | VARCHAR | NOT NULL
**song_id** | VARCHAR |
**artist_id** | VARCHAR |
**session_id** | INT | NOT NULL
**location** | VARCHAR |
**user_agent** | VARCHAR |

Sample...

**songplay_id** | **start_time** | **user_id** | **level** | **song_id** | **artist_id** | **session_id** | **location** | **user_agent**
----------- | ---------- | ------- | ----- | ------- | --------- | ---------- | -------- | ----------
5449 | 2018-11-21 21:56:47.796000 | 15 | paid | SOZCTXZ12AB0182364 | AR5KOSW1187FB35FF4 | 818 | Chicago-Naperville-Elgin, IL-IN-WI | "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/36.0.1985.125 Chrome/36.0.1985.125 Safari/537.36"

........................................................................................................................

### Table: users

**Column name** | **Data type** | **Column description**
----------- | --------- | ------------------
**user_id**  | INT | PRIMARY KEY, NOT NULL
**first_name** | VARCHAR | NOT NULL
**last_name** | VARCHAR | NOT NULL
**gender** | VARCHAR |
**level** | VARCHAR |

Sample...

**user_id** | **first_name** | **last_name** | **gender** | **level**
------- | ---------- | --------- | ------ | -----
15      | Lily       | Koch      | F      | paid

........................................................................................................................

### Table: songs

**Column name** | **Data type** | **Column description**
----------- | --------- | ------------------
**song_id**  | VARCHAR | PRIMARY KEY, NOT NULL
**title** | VARCHAR | NOT NULL
**artist_id** | VARCHAR | NOT NULL
**year** | VARCHAR |
**duration** | VARCHAR |

Sample...

**song_id** | **title** | **artist_id** | **year** | **duration**
----------- | -------------- | ------------- | ---------- | ---------
SOZCTXZ12AB0182364 | Setanta matins | AR5KOSW1187FB35FF4 | 0 | 269.58322

........................................................................................................................

### Table: artists

**Column name** | **Data type** | **Column description**
--------------- | ------------- | ----------------------
**artist_id**  | VARCHAR | PRIMARY KEY, NOT NULL
**name** | VARCHAR | NOT NULL
**location** | VARCHAR | NOT NULL
**latitude** | VARCHAR |
**longitude** | VARCHAR |

Sample...

**artist_id** | **name** | **location** | **latitude** | **longitude**
------------- | -------- | ------------ | ------------ | -------------
AR5KOSW1187FB35FF4 | Elena | Dubai UAE | 49.80388 | 15.47491

........................................................................................................................

### Table: time

**Column name** | **Data type** | **Column description**
--------------- | ------------- | ----------------------
**start_time**  | VARCHAR | NOT NULL
**hour** | VARCHAR | NOT NULL
**day** | VARCHAR | NOT NULL
**week** | VARCHAR | NOT NULL
**month** | VARCHAR | NOT NULL
**year** | VARCHAR | NOT NULL
**weekday** | VARCHAR | NOT NULL

Sample...

**start_time** | **hour** | **day** | **week** | **month** | **year** | **weekday**
-------------- | -------- | ------- | -------- | --------- | -------- | -----------
2018-11-21 21:56:47.796000 | 21 | 21 | 47 | 11 | 2018 | 2

........................................................................................................................
