import tarfile

import datetime
import threading

import os

import database

from boto.s3.connection import S3Connection
from boto.s3.key import Key

S3_BUCKET_NAME = "sensor_visualization_backup"
AWS_ACCESS_KEY = "Sensor"
AWS_SECRET_ACCESS_KEY = "Visualization"

# backup interval is 24 hours
BACKUP_INTERVAL = 60 * 60 * 24

def setup():
    """ initialize a backup thread and start running it """
    thread = threading.Thread(target = backup)
    thread.start()

def run():
    """ backup the database every 24 hours, starting now """
    event = threading.Event()
    while (event.is_set() == False):
        # perform database backup
        backup()

        # sleep for the predefined amount interval
        event.wait(BACKUP_INTERVAL)

def save_file_in_s3(filename):
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(S3_BUCKET_NAME)
    k = Key(bucket)
    k.key = filename
    k.set_contents_from_filename(filename)

def get_archive_filename():
    """ return the archive name (today's date) """
    today = datetime.date.today()
    return str(today)

def archive(mongo_backup_file):
    """ gzip the file and return the filename """
    filename = get_archive_filename()
    tar = tarfile.open(filename, "w|gz")
    tar.add(mongo_backup_file)
    tar.close()

    return filename

def backup():
    # dump the collection to a dedicated folder
    path = database.dump_database_to_file()

    # archive the path to a gzip file
    filename = archive(path)

    # backup to S3
    save_file_in_s3(filename)
