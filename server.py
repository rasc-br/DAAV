''' server.py '''

import json
import logging as log
import configparser
from datetime import datetime, timedelta
# from functools import wraps
from flask import (Flask, jsonify, request, current_app) # Response, Blueprint
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
import jwt
import database as db
import base64

CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')

TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "APK scanner API",
        "description": "An API that scans APKs looking for security vulnerabilities",
        "contact": {
            "responsibleOrganization": "ISCTE - Instituto Universitário de Lisboa",
            "responsibleDeveloper": "Carlos Serrão",
            "email": "carlos.serrao@iscte-iul.pt",
            "url": "istar.iscte-iul.pt",
        },
        "termsOfService": "http://me.com/terms",
        "version": "0.0.1"
    },
    "host": "127.0.0.1:5000",  # overrides localhost:500
    "basePath": "/",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "operationId": "getmyData"
}

# Create the application instance
app = Flask(__name__, template_folder="templates")
Swagger(app, template=TEMPLATE)

log.basicConfig(filename=CONFIG['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

app.config.update(
    TESTING=True,
    SECRET_KEY='RaphaelAlexandreSperandioCandello'
)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Create a URL route in our application for "/"
# This is purely to see if the server is running, there is currently no website planned
@app.route('/')
def home():
    return jsonify({'status': True, 'message': 'API is responding... keep trying!'}), 200


@app.route('/apkscan', methods=['POST'])
@swag_from('./docs/apkscan.yml')
def apkscan():
    log.debug("APKSCAN REQUEST RECEIVED")
    data = request.values

    # check if an MD5 has been passed
    if "md5" not in data:
        return jsonify({'status': False, 'message': 'Hey...! Where is my MD5???'}), 200, {'Access-Control-Allow-Origin':'*'}
    else:
        md5Apk = data["md5"]
        log.debug("APK MD5 = " + md5Apk)
        # 1. add the apk to scan to the database
        if db.apk_id_exists(md5Apk, 'apkresults'):
            return jsonify({'status': False,
                            'message': 'That APK was previously processed and exists on the results database. Please check the results using the appropriate API call!'}), 200, {'Access-Control-Allow-Origin':'*'}
        else:
            if db.apk_id_exists(md5Apk, 'apk2scan'):
                return jsonify({'status': False, 'message': 'That APK is already in the pipeline to be processed... wait for the results!'}), 200, {'Access-Control-Allow-Origin':'*'}
            else:
                db.insert_new_apk2scan(md5Apk)
                return jsonify({'status': True, 'message': 'APK was passed to the scanning engine... please hold on!'}), 200, {'Access-Control-Allow-Origin':'*'}


@app.route('/apkfeedback/<id>', methods=['GET'])
@swag_from('./docs/apkfeedback.yml')
def apkfeedback(id):
    log.debug("APKSCAN REQUEST RECEIVED")
    log.debug("APK MD5 = " + id)
    if not id:
        return jsonify({'status': False, 'message': 'No MD5 APK id was passed'}), 500, {'Access-Control-Allow-Origin':'*'}
    else:
        results_data = db.get_apk_status(id)
        if results_data:
            # we need to check the status...
            if results_data[0]['status'] != -1:
                print(results_data[0]['results_location'])
                file = open(results_data[0]['results_location'])
                json_data = json.load(file)
                return jsonify({'status': True, 'results_history': results_data, 'results': json_data}), 200, {'Access-Control-Allow-Origin':'*'}
            else:
                return jsonify({'status': False, 'message': results_data[0]['details']}), 500, {'Access-Control-Allow-Origin':'*'}
        else:
            return jsonify({'status': False, 'message': 'APK work was not finished... please come back l8r!'}), 500, {'Access-Control-Allow-Origin':'*'}

@app.route('/register/', methods=('POST',))
def register():
    data = request.get_json(silent=True)
    print('Received ', data.get('username'), ' and password.')

    register_user = db.register_user(data.get('username'), data.get('password'), 'none')

    if register_user == 'SUCCESS':
        print('User ', data.get('username'), ' registered!')
    else:
        print('Error registering user in database')
    return register_user


@app.route('/login/', methods=('POST',))
def login():
    data = request.get_json(silent=True)
    print('Check ', data.get('username'), ' login.')

    login_result = db.login_user(data.get('username'), data.get('password'))

    if (login_result == 'FAIL'):
        return login_result
    else:
        token = jwt.encode({
            'sub': login_result['username'],
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=60)},
            current_app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8'),
                        'username': login_result['username'],
                        'email': login_result['email'],
                        'firstname': login_result['firstname'],
                        'lastname': login_result['lastname'],
                        'address': login_result['address'],
                        'city': login_result['city'],
                        'country': login_result['country'],
                        'about': login_result['about'],
                        'type': login_result['level'],
                        'imgtype': login_result['imgtype'],
                        'postalcode': login_result['postalcode'],
                        'avatar': login_result['profileimg']
                       })

@app.route('/edit_profile/', methods=('POST',))
def edit_profile():
    data = request.get_json(silent=True)

    edited_profile = db.edit_profile(data)

    if edited_profile == 'SUCCESS':
        print('Profile ', data.get('username'), ' edited!')
    else:
        print('Error editing profile in database')
    return edited_profile

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
