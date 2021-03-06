''' database.py '''

import configparser
import logging as log
import json
import pymysql
import datetime
import base64
from werkzeug.security import generate_password_hash, check_password_hash

config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

def insert_results(md5, tool, results_location, status, details, apk_name):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apkresults (md5, scantool, results_location, status, details, created_at, apk_name) VALUES ('%s', '%s', '%s', '%s', '%s', NOW(), '%s')" % (md5, tool, results_location, status, details, apk_name)
    log.debug(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        return False
    db.close()


def insert_new_apk2scan(md5,username):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apk2scan (md5, created_at, username) VALUES ('%s', NOW(), '%s')" % (md5, username)
    log.debug(sql)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        return False
    db.close()


def get_all_apk2scan():
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM apk2scan"
    log.debug(sql)
    cursor.execute(sql)
    apks = cursor.fetchall()
    db.close()
    return apks


def delete_apk2scan(md5):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "DELETE FROM apk2scan WHERE md5 = '" + md5 + "'"
    log.debug(sql)
    cursor.execute(sql)
    db.commit()
    db.close()


def insert_new_apk(md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile, username):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apk (md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile, status, created_at, updated_at, username) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s, NOW(), NOW(), '%s')" % \
          (md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile, 1, username)
    log.debug(sql)
    try:
        # print(sql)
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        return False
    db.close()


def apk_id_exists(md5, table):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM " + table + " WHERE md5 = '" + md5 + "'"
    log.debug(sql)
    cursor.execute(sql)
    if cursor.fetchone():
        return True
    else:
        return False


def get_apk_status(md5):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM apkresults WHERE md5 = '" + md5 + "' ORDER BY id DESC LIMIT 1"
    log.debug(sql)
    cursor.execute(sql)
    json_data = []
    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    for result in results:
        json_data.append(dict(zip(row_headers, result)))
    db.close()
    return json_data

def register_user(username, password, email):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    hashed_password = generate_password_hash(password, method='sha256')
    sql = "INSERT INTO users (username, password, email, status, level, created) VALUES ('%s', '%s', '%s', 'active', '1', NOW())" % (username, hashed_password, email)
    log.debug(sql)
    try:
        cursor.execute(sql)
        db.commit()
        return 'SUCCESS'
    except (pymysql.Error, pymysql.Warning) as e:
        print(e)
        # print(e.args[0])
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        if e.args[0] == 1062:
            return 'This user is already registered'
        else:
            return 'Database error'
    db.close()


def login_user(username, password):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM users WHERE username = '" + username + "' ORDER BY id DESC LIMIT 1"
    log.debug(sql)
    try:
        cursor.execute(sql)
        row_headers = [x[0] for x in cursor.description]
        result = cursor.fetchone()
        if (result):
            dict_data = dict(zip(row_headers, result))
            # json_data = json.dumps(dict_data)
            # json_data contains all user information collected from db
            db.close()
            passord_ok = check_password_hash((dict_data['password']), password)
            if passord_ok:
                print("Username and Password OK!")
                return dict_data
            else:
                print("Login failed")
                return 'FAIL'
        else:
            return 'FAIL'
    except (pymysql.Error, pymysql.Warning) as e:
        print(e)
        # print(e.args[0])
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        if e.args[0] == 1062:
            return 'This user is already registered'
        else:
            return 'Database error'
    db.close()


def edit_profile(data):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = """UPDATE users SET profileimg = '%s', imgtype = '%s', email = '%s', firstname = '%s', lastname = '%s', address = '%s',
             city = '%s', country = '%s', postalcode = '%s', about = '%s'
             WHERE username = '%s'
             """ % (data.get('avatar'), data.get('imgtype'), data.get('email'), data.get('firstname'), data.get('lastname'), data.get('address'),
                    data.get('city'), data.get('country'), data.get('postalcode'), data.get('about'),
                    data.get('username'))

    try:
        cursor.execute(sql)
        db.commit()
        return 'SUCCESS'
    except (pymysql.Error, pymysql.Warning) as e:
        print(e)
        db.rollback()
        return 'Database error'
    db.close()

def convertSQLResult(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def get_all_results(username):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "SELECT * FROM apkresults WHERE username = '" + username + "' ORDER BY id"
    # Consider order by app name (save in apkresults app name)
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()

    dict_data = [dict(zip([key[0] for key in cursor.description], row)) for row in result]

    for item in dict_data:
        item['result_b64'] = (base64.b64decode(item['result_b64'])).decode()
        item['result_b64'] = json.loads(item['result_b64'])
    # dict_data['result_b64'] = base64.b64decode(dict_data['result_b64'])
    json_data = json.dumps(dict_data, default = convertSQLResult)

    return json_data