''' manager.py '''

import os
from urllib.parse import urlparse
import math
import json
import configparser
import logging as log
from sys import platform
import requests
from tqdm import tqdm
import database as db

config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

aptoide_API_endpoint = config['DOWNLOAD']['aptoideAPIEndpoint']

dir = config['DOWNLOAD']['apkDownloadDir']
json_dir = config['DOWNLOAD']['jsonDir']
   
def download_apk(app2download):
    # check if the download dir exists or not
    print ('Operational system:'+platform) # linux / linux2 / win32 / darwin
    if not os.path.exists(dir):
        os.mkdir(dir)

    # write the file to the filesystem
    a = urlparse(app2download)
    filename = dir + "/" + os.path.basename(a.path)

    if (os.path.isfile(filename)):
        print ('File already downloaded')
    else:
        # Streaming, so we can iterate over the response.
        r = requests.get(app2download, stream=True)

        # Total size in bytes.
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024
        wrote = 0
        with open(filename, 'wb') as f:
            for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size // block_size), unit='KB',
                            unit_scale=True):
                wrote = wrote + len(data)
                f.write(data)
        if total_size != 0 and wrote != total_size:
            print("ERROR, something went wrong")


def get_json_data(which_apk):
    response = requests.get(aptoide_API_endpoint + which_apk)
    jsoninfo = response.json()
    return jsoninfo


def write_json_data(jsonData, whick_apk):
    if not os.path.exists(json_dir):
        os.mkdir(json_dir)

    filename = json_dir + "/" + whick_apk + ".json"
    print ('write filename:'+filename)
    with open(filename, 'w') as f:
        f.write(json.dumps(jsonData))
    f.close()
    return True


if __name__=="__main__":
    VERSION = '0.1'
    banner = "APK Downloader"
    print(str(banner))

    log.debug("------------------------")
    log.debug("APPSENTINEL MANAGER HAS BEEN INVOKED!!!!")

    # 1. Go to the database and check if there are APKs to download
    apks = db.get_all_apk2scan()
    # 2. For each APK on the database, download it locally, add to the apk table and delete from the table
    if apks:
        for apk in apks:
            jsondata = get_json_data(apk[1])
            username = apk[3]
            # check what is the return of the API call -> check if the APK exists!!!
            if jsondata["info"]["status"] == "FAIL":
                # that APK can't be found
                log.debug("This APK doesn't exist on APTOIDE -> APK = " + apk[1])
                db.delete_apk2scan(apk[1])
                db.insert_results(apk[1], "", "", -1, "This APK does not exist, or it could not be downloaded from the Aptoide app store!", 'none')
            else:
                applicationName = jsondata["nodes"]["meta"]["data"]["name"]
                applicationPackage = jsondata["nodes"]["meta"]["data"]["package"]
                appVersion = jsondata["nodes"]["meta"]["data"]["file"]["vername"]
                appMD5 = jsondata["nodes"]["meta"]["data"]["file"]["md5sum"]
                appPath = jsondata["nodes"]["meta"]["data"]["file"]["path"]
                apkfile = appPath[appPath.rfind("/") + 1:]
                print("Getting the following APK => " + applicationName)
                log.debug("Getting the following APK => " + applicationName)
                print(applicationPackage + " (" + appVersion + ") -> " + appMD5)
                log.debug(applicationPackage + " (" + appVersion + ") -> " + appMD5)
                print(appPath)
                log.debug(appPath)
                download_apk(appPath)
                write_json_data(jsondata, apk[1])
                db.insert_new_apk(apk[1], applicationName, applicationPackage, appVersion, appPath, apkfile, username)
                print("\n")
                # log.debug(config['GENERAL']['python3cmd'] + " scanner.py --md5 " + appMD5 + " --file " + dir + "/" + apkfile)
                print("GO SCANNER (Python 2) »» "+config['GENERAL']['python2cmd'] + " scanner_py2plugins.py --md5 " + appMD5 + " --user " + username + " --file " + dir + "/" + apkfile)
                os.system(config['GENERAL']['python2cmd'] + " scanner_py2plugins.py --md5 " + appMD5 + " --user " + username + " --file " + dir + "/" + apkfile)

                print("GO SCANNER (Python 3) »» "+config['GENERAL']['python3cmd'] + " scanner_py3plugins.py --md5 " + appMD5 + " --user " + username + " --file " + dir + "/" + apkfile)
                os.system(config['GENERAL']['python3cmd'] + " scanner_py3plugins.py --md5 " + appMD5 + " --user " + username + " --file " + dir + "/" + apkfile)

                db.delete_apk2scan(apk[1])
                print("\n")
                print("Manager DONE!")
    else:
        print("No apks yet... waiting patiently!!!")
        log.debug("No apks yet... waiting patiently!!!")
