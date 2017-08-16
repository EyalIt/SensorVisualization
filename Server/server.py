import pygal
from flask import Flask, render_template, request
from pygal.style import DarkSolarizedStyle
from werkzeug.utils import redirect

from Server import database

# web service to respond to get and post requests
__web_service = Flask("SensorVisualization")

def start(url, port):
    """ get a url and port address and start listening to requests """

    # create the database
    database.init_database(__web_service)

    # initiate the web service
    __web_service.run(debug = False, host = url, port = port, threaded = True)

@__web_service.route('/update_sensors', methods=['POST'])
def update_sensors():
    """ get a request from a user in a JSON format (according to the keys defined in json_keys file)
        create a document, that includes also the user id, and add it to the database """

    # parse the JSON object in the request
    content = request.get_json(silent = True)
    remote_user = request.remote_addr

    # add the document to the database
    database.insert_document(content, remote_user)

    # dispatch response
    return __web_service.make_response("great! the document was added successfully to the database")

@__web_service.route('/query_sensors/', methods=['GET', 'POST'])
def query_sensors():
    """ generate a histogram of the sensor values, according to the sensor type and user input """

    # get the enumeration of the sensors
    options = database.enumerate_sensors()
    sensor_type = options[0]

    # get the enumeration of the users
    users = database.enumerate_users()
    user = users[0]

    # get the input from the web request
    if request.method == 'POST':
        sensor_type = request.form['sensor_type']
        user = request.form['user']

    # generate the histogram based on user and sensor type
    bar_chart = get_bar_chart(sensor_type, user)

    # return the html object
    return render_template('SensorQuery.html', users = users, default_user = user,
                           options = options, default_sensor = sensor_type, bar_chart = bar_chart)

def get_bar_chart(sensor_type, user):
    """ generate histogram, according to the data extracted from the database """
    (labels, data) = database.get_sensor_value_distribution(sensor_type, user)

    # create a bar chart
    title = sensor_type + " Histogram For User " + user
    bar_chart = pygal.Bar(width = 900, height = 500,
                          explicit_size = True, title = title, style = DarkSolarizedStyle)

    bar_chart.x_labels = labels
    bar_chart.add('# Samples', data)

    return bar_chart