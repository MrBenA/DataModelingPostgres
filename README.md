# SparkifyDB

## Overview
Sparkify offers a music streaming service through desktop and hand-held devices.<br>
To enable Sparkify to analyse data collected though their music streaming applications, Sparkify wish to establish<br>
a relational analytical database to gain insight from the songs played by their user-base.

---

## Datasets
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

### Table Schema and samples

#### Table: **songplays**

Column name | Data Type | Column description
----------- | --------- | ------------------
songplay_id  | INT |
start_time | TIMESTAMP |
user_id | VARCHAR | NOT NULL
level | VARCHAR |
song_id | VARCHAR |
artist_id | VARCHAR |
session_id | INT |
location | VARCHAR |
user_agent | VARCHAR |
