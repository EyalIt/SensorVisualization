import tarfile
import datetime
import threading
import boto3 as boto3
import database


S3_BUCKET_NAME = r"sensorvisualization"

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
    try:
        # create the s3 client and upload the file
        s3_client = boto3.client('s3')
        s3_client.upload_file(filename, S3_BUCKET_NAME, filename)
    except Exception, err:
        print err

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
