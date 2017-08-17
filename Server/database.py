import datetime

import subprocess

import os
from flask_pymongo import PyMongo
import json
import document

# path to mongodump external tool
from Server import database_backup

MONGODUMP_PATH = r"C:\Program Files\MongoDB\Server\3.4\bin"

__database = None

def init_database(web_service):
    """ initialize a mongoDB database """
    with web_service.app_context():
        global __database
        mongo = PyMongo(web_service, config_prefix = 'MONGO')

        __database = mongo.db

        database_backup.setup()

def get_collection():
    """ get the collection for the current day """
    collection = datetime.date.today()
    return __database.sensors[collection]

def get_collection_to_backup():
    """ get the collection from yesterday, as this should be sent to S3 server for backup """
    collection = datetime.date.today() - datetime.timedelta(1)
    return __database.sensors[collection]

def insert_document(json_str, remote_addr):
    """ get a JSON object and the remote address of the user who generated the sensor inputs.
        creates a document and add it to the database """
    # extract the data from the user request and generate a database JSON object
    sample = json.loads(json_str)[0]
    doc = document.create(sample, remote_addr)

    # add the document to the database
    collection = get_collection()
    collection.insert_one(doc)

def get_sensor_value_distribution(sensor, user):
    """ get the sensor type and user identifier (ip number) and return distribution
        of the sensor samples received by the user. the distribution is sorted in 10 buckets """
    collection = get_collection()

    # query the database and group by sensor value
    posts = collection.aggregate([
        {'$match': {document.DOC_CLIENT_ID_KEY: {'$eq': user}}},
        { '$match' : {document.DOC_SENSOR_DATA_KEY + '.' + document.DOC_SENSOR_ORIGIN_KEY : {'$eq' : sensor}} },
        { '$bucketAuto' : {
            'groupBy' : "$" + document.DOC_SENSOR_DATA_KEY + '.' + document.DOC_SENSOR_VALUE_KEY,
            'buckets' : 10
            }
        }
    ])

    # extract the labels and data for easier display
    labels = []
    data = []
    for post in posts:
        labels.append(str(post['_id']['min']) + " - " + str(post['_id']['max']))
        data.append(post['count'])

    return (labels, data)

def enumerate_sensors():
    """ enumerate all the sensor types """
    collection = get_collection()

    sensors = collection.distinct(document.DOC_SENSOR_DATA_KEY + '.' + document.DOC_SENSOR_ORIGIN_KEY)
    return sensors

def enumerate_users():
    """ enumberate all the users in the database """
    collection = get_collection()

    users = collection.distinct(document.DOC_CLIENT_ID_KEY)
    return users

def delete_collection(collection):
    """ delete a collection from the database (the assumption is that it is backed up in S3 server """
    collection.delete_many({})

def dump_database_to_file():
    """ backup an unused collection and store it in a folder. use mongodump external tool """
    collection = get_collection_to_backup()

    # get the database and collection name to backup
    name = collection.full_name
    split = name.split('.', 1)
    db_name = split[0]
    collection_name = split[1]

    # the path to backup to
    path = os.path.abspath(os.path.join(os.path.curdir, name))

    try:
        # execute mongodump and backup the database to external directory
        backup_output = subprocess.check_output(
            [
                MONGODUMP_PATH + '\mongodump',
                '--db', '%s' % db_name,
                '--collection', '%s' % collection_name,
                '--out', '%s' % path
            ])

        # delete the collection after it is backed up
        #delete_collection(collection)

        return path
    except Exception, err:
        print err
        return None