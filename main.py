"""This module is called by Google App Engine

It looks for "app" in the "main.py" class to run flask with gunicorn"""

import time
import logging
from pandas import DataFrame
from flask import Flask, render_template, request, send_file, make_response ,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask.logging import create_logger
from sqlalchemy.sql.expression import column

from models import Base, Data, Records
import test_gets as gets

user = "challenger"
password = "not_the_real_password"
dbname = "coding-challenge-db"
host = "34.84.8.142"


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


@app.route('/test_db', methods=['GET'])
def test_db():
    data = session.query(Records).filter_by(id=5).all()
    return jsonify(f'this connected to the db {data}')


@app.route('/test/<int:item_count>', methods=['GET'])
def at_test(item_count=None):
    """Runs when GET requested on '/login/<user_id>'.

    The main endpoint to test the time it takes to process the items in the database.

    Args:
        item_count=None (str): sets the number of items to count after the '/test/' path

    Return:
        render_template (flask): html template based on logic from this app"""
    log.info("@ at_test(item_count=None): %s", item_count)

    #  ˅This is the script that measures the performance, not allowed to edit this section.˅ 
    hit_time = time.time()
	#  ˄This is the script that measures the performance, not allowed to edit this section.˄ 

    # <- get email query string
    person_query = request.args.get('person', type = str)

    type_query = request.args.get('type', type = str)

    # <- get user info
    response = gets.get_table("records")
    if isinstance(response, Exception):
        return render_template('at-error.html', message="There was an error.", error=response)

    records_json = response["records_table"].to_json(orient="records")

    response2 = gets.get_table("data")

    if item_count > 100:

        return render_template(
            'at-error.html',
            message="More then 100 items selected, too many. Item Count: ",
            error=item_count)

    if (type_query == "text"):

        data_text = response2["data_table"].to_json(orient="records")

        return render_template(
            'at-text.html',
            records=records_json,
            data=data_text,
            item_count=item_count,
            hit=hit_time)
    
    data_json = response2["data_table"].to_json(orient="records")

    return render_template(
        'at-json.html',
        records=records_json,
        data=data_json,
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
