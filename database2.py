''' database.py '''

import ConfigParser
import logging as log
import datetime
import pymysql
import base64

config = ConfigParser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config.get('GENERAL', 'logDir') + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

def insert_results(md5, tool, results_location, status, details, json_result, apk_name, username):
    db = pymysql.connect(config.get('MYSQL', 'host'), config.get('MYSQL', 'user'), config.get('MYSQL', 'password'),
                         config.get('MYSQL', 'database'))
    print("Inserting Results of:"+tool)
    print (type(json_result))
    cursor = db.cursor()
    now = datetime.datetime.now()
    b64_result = base64.b64encode(json_result)

    sql = "INSERT INTO apkresults (md5, scantool, results_location, status, details, created_at, apk_name, username, result_b64) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (md5, tool, results_location, status, details, now, apk_name, username, b64_result)  
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        log.debug("AN ERROR OCCURED WHILE INSERTING DATA -> " + sql)
        db.rollback()
        return False
    db.close()
