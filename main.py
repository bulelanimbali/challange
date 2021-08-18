"""This module is called by Google App Engine

It looks for "app" in the "main.py" class to run flask with gunicorn"""

from flask import Flask, render_template, request
from flask.logging import create_logger
from models import Base, Data, Records 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from configparser import ConfigParser
import old_db_files.test_gets as gets
import logging
import time
import json

cfg = ConfigParser()
cfg.read('database.ini')

user = cfg.get('postgresql','user')
password= cfg.get('postgresql','password')
dbname= cfg.get('postgresql','dbname')
host= cfg.get('postgresql','host')

# I get a Higher score when it is stored in the main file 
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:5432/{dbname}')


Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
log = create_logger(app)
log.info('------ DEBUG LOGGING STARTS HERE -------')


@app.route('/', methods=['GET'])
def index():
    """Runs when GET requested on '/'.

    Returns:
        render_template (flask): index.html
    """
    log.info("@ index()")

    return render_template(
        'at-index.html')


#this is not in use
@app.route('/log', methods=['GET'])
def at_log():
    """Runs when GET requested on '/log'.
    
    When user selects view log from the home page.
    
    Return:
        render_template (flask): html template based on logic from this app
    """
    log.info("@ at_log()")

    response = gets.get_table()
    if isinstance(response, Exception):
        return render_template('at-error.html', message=".error('Error occured')", error=response)

    database_log_html = response["data_table"].to_html(index=False)

    return render_template(
        'at-log.html',
        data=database_log_html)

@app.route('/test/<int:item_count>', methods=['GET'])
def at_test(item_count=None):
    """
    DESC:
        The main endpoint to test the time it takes to process the items in the database.

    Args:
        item_count=None (str): sets the number of items to count after the '/test/' path

    Return:
        render_template (flask): html template based on logic from this app
    """
    log.info("@ at_test(item_count=None): %s", item_count)

    #  ˅This is the script that measures the performance, not allowed to edit this section.˅ 
    hit_time = time.time()
	#  ˄This is the script that measures the performance, not allowed to edit this section.˄ 

    person_query = request.args.get('person', type = str)
    type_query = request.args.get('type', type = str)
    data = session.query(Data, Records).outerjoin(Data, Records.data_id==Data.id)\
        .filter(Records.person==person_query).limit(item_count)

    if type_query == 'text':
        text_json =  [i[0].text for i in data]
        type = 'text'
    else:
        text_json =  [i[0].json for i in data]
        type = 'json'

    print(type_query)
    json_records = json.loads(json.dumps({
        'type':type,
        "id":[i[0].id for i in  data],
        "json_text": text_json,
        'person': data[0][1].person
    }))
    
    return render_template(
        'at-json.html',
        records=json_records,
        item_count=item_count,
        hit=hit_time)

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google app
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # app Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
