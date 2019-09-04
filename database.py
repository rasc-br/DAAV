''' database.py '''

import pymysql
import configparser
import logging as log

config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

def insert_results(md5, tool, results_location, status, details):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apkresults (md5, scantool, results_location, status, details, created_at) VALUES ('%s', '%s', '%s', '%s', '%s', NOW())" % (md5, tool, results_location, status, details)
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


def insert_new_apk2scan(md5):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apk2scan (md5, created_at) VALUES ('%s', NOW())" % (md5)
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


def insert_new_apk(md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile):
    db = pymysql.connect(config['MYSQL']['host'], config['MYSQL']['user'], config['MYSQL']['password'],
                         config['MYSQL']['database'])
    cursor = db.cursor()
    sql = "INSERT INTO apk (md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile, status, created_at, updated_at) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %s, NOW(), NOW())" % \
          (md5, applicationName, applicationPackage, applicationVersion, applicationPath, apkFile, 1)
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
    sql = "INSERT INTO users (username, password, email, status, level, created) VALUES ('%s', '%s', '%s', 'active', '1', NOW())" % (username, password, email)
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
        # if e.args[0] == PYMYSQL_DUPLICATE_ERROR:
        #  return 'Duplicate username'
        # else:
        #  return 'FAIL'
    db.close()


