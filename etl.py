import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Extracts song and artist data from JSON files to dataframes and executes table insert statements.
    """

    # Read song file to dataframe.
    df = pd.read_json(filepath, lines=True)

    # Create song data dataframe and execute song table SQL insert statement.
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)

    # Create artist data dataframe and execute artist table SQL insert statement.
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[
        0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Extracts song and artist data from JSON files to dataframes and executes table insert statements.
    """

    # Read activity log file to dataframe.
    df = pd.read_json(filepath, lines=True)

    # Filter dataframe by 'NextSong' action.
    nxtsong_df = df.loc[(df.page == 'NextSong')]

    # Convert timestamp column to datetime.
    t = pd.to_datetime(nxtsong_df['ts'], unit='ms')

    # Create time data dictionary from dataframe and execute table SQL insert statement.
    time_data = [t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_dict = {column_labels[i]: time_data[i] for i in range(len(column_labels))}
    time_df = pd.DataFrame.from_dict(time_dict)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # Create user data dataframe and execute table SQL insert statement.
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates().dropna()

    # Iterate through records of user dataframe and execute SQL insert statement.
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # Iterate through log file dataframe for songplay data.
    for index, row in df.iterrows():

        # Get songid and artistid from joined song and artist tables.
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # Create songplay tuple and execute SQL insert statement.
        songplay_data = (
            pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location,
            row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Determines data files for processing, iterates and processes each file.
    """

    # Create list of files matching extension from directory.
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # Get total number of files found.
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # Iterate over each file found and process.
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Create database connection and runs song and log file data processing functions when ETL file is run.
    """

    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
