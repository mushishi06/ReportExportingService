# import json

from dicttoxml import dicttoxml

from flask import Flask, json, jsonify, make_response, request

from pdf import create_pdf

import psycopg2

# Deffine which config to use, see config.py for the other
APP_SETTINGS = "config.DevelopmentConfig"

app = Flask(__name__)
# call the config for our application
app.config.from_object(APP_SETTINGS)

# Define our connection string in the config
conn_string = app.config['CONN_STRING']

# print the connection string we will use to connect
print ("Connecting to database\n ->%s" % (conn_string))

# get a connection, if a connect cannot be made an exception will be raised here
try:
    conn = psycopg2.connect(conn_string)
except Exception as e:
    error = "Error connecting database: {}".format(str(e))
    # print(error)
    exit(error)

# conn.cursor will return a cursor object, you can use this cursor to perform queries
cursor = conn.cursor()
print ("Connected!\n")


@app.errorhandler(404)
def not_found(error=None):
    """Error handler 404."""
    message = {'status': 404, 'message': 'Not Found:' + request.url}
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.route('/', methods=['GET', 'POST'])
def index():
    """Define the main route for the API (usage)."""
    return make_response('Usage: /reports/{int:reports_id} <br>Eg. /reports/2?format=pdf<br>Eg. /reports/2?format=xml<br><br>Usage: /reports <br>Eg. /reports?format=pdf<br>Eg. /reports?format=xml')


@app.route("/reports/<int:reports_id>", methods=['GET'])
def get_report_by_id(reports_id):
    """Route for reports."""
    if 'Content-Type' in request.headers and request.headers['Content-Type'] in app.config['SUPPORTED_CONTENT_TYPE']:
        if request.headers['Content-Type'] == 'application/pdf':
            ext = 'pdf'
        elif request.headers['Content-Type'] == 'text/xml':
            ext = 'xml'
        elif request.headers['Content-Type'] == 'application/json':
            ext = 'json'
    elif 'format' in request.args and request.args['format'] in app.config['SUPPORTED_FORMAT']:
        ext = request.args['format']
    else:
        ext = 'json'

    cmd = "SELECT * FROM reports WHERE id = %s;" % reports_id
    # execut the cmd for fetch the correct data.
    cursor.execute(cmd)
    # fetch the data from the Database.
    data = cursor.fetchone()
    if not data:
        return not_found()

    jdata = decode_data(data)
    if ext == 'pdf':
        # Generate the pdf
        pdf, filename = create_pdf(reports_id, jdata['data'])
        # Set the pdf data as responce
        resp = make_response(pdf)
        # Set the header as pdf
        resp.headers["Content-Type"] = 'application/pdf'
        return resp
    if ext == 'xml':
        # Create the xml
        xml = dicttoxml(jdata, custom_root='Report', attr_type=False)
        # Set the xml data as responce
        resp = make_response(xml)
        # Set the header as xml
        resp.headers["Content-Type"] = 'text/xml'
        return resp
    if ext == 'json':
        # Create the json
        resp = make_response(json.dumps(jdata))
        # Set the header as json
        resp.headers["Content-Type"] = 'application/json'
        return resp
    return "Nay!", 202


def decode_data(data):
    """Decode and clean the data."""
    new_data = {}
    try:
        new_data['id'] = data[0]
        new_data['data'] = json.loads(data[1])
        return new_data
    except Exception:
        new_data['id'] = data[0]
        new_data['data'] = data[1]
        return new_data


@app.route("/reports", methods=['GET'])
def get_reports():
    """Route for reports."""
    if 'Content-Type' in request.headers and request.headers['Content-Type'] in app.config['SUPPORTED_CONTENT_TYPE']:
        if request.headers['Content-Type'] == 'application/pdf':
            ext = 'pdf'
        elif request.headers['Content-Type'] == 'text/xml':
            ext = 'xml'
        elif request.headers['Content-Type'] == 'application/json':
            ext = 'json'
    elif 'format' in request.args and request.args['format'] in app.config['SUPPORTED_FORMAT']:
        ext = request.args['format']
    else:
        ext = 'json'

    cmd = "SELECT * FROM reports;"
    # execut the cmd for fetch the correct data.
    cursor.execute(cmd)
    # fetch the data from the Database.
    data = cursor.fetchall()
    if not data:
        return not_found()
    # clean the data
    jdata = list(map(decode_data, data))
    if ext == 'pdf':
        # Generate the pdf
        pdf, filename = create_pdf('all', jdata)
        # Set the pdf data as responce
        resp = make_response(pdf)
        # Set the header as pdf
        resp.headers["Content-Type"] = 'application/pdf'
        return resp
    if ext == 'xml':
        print('jData: ', jdata)
        # Create the xml
        xml = dicttoxml(jdata, custom_root='Reports', attr_type=False)
        # Set the xml data as responce
        resp = make_response(xml)
        # Set the header as xml
        resp.headers["Content-Type"] = 'text/xml'
        return resp
    if ext == 'json':
        # Create the json
        resp = make_response(json.dumps(jdata))
        # Set the header as json
        resp.headers["Content-Type"] = 'application/json'
        return resp
    return "Nay!", 202


if __name__ == '__main__':
    app.run()
