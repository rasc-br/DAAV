# vulnScanManager, will be responsible for checking a specific directory for apks and for processing them!
# -*- coding: UTF-8 -*-
from __future__ import absolute_import
import os.path
import argparse
import configparser
import sys
import database3 as db
import json
import ast

config = configparser.ConfigParser()
config.read('config.ini')

jsonResultsLocation = config['SCANNER']['jsonResultsLocation']
apkDownloadedFolder = config['DOWNLOAD']['apkDownloadDir']
dictionaryOWASP = config['DICTIONARY']['owasp']

class Results(object):
    def __init__(self, plugin=None, jsonResult=None):
        self.plugin = plugin
        self.jsonResult = jsonResult

def flatten_dict(dd, separator ='_', prefix =''): 
    return { prefix + separator + k if prefix else k : v 
             for kk, vv in dd.items() 
             for k, v in flatten_dict(vv, separator, kk).items() 
             } if isinstance(dd, dict) else { prefix : dd } 

def listPlugins():
    print("These are the available plugins:")
    for m in plugins:
        print("\n"+m.pluginName+"\n")

def runPlugins():
    print("Running all the available plugins:")
    for analizePugin in plugins:
        print ("\n Executing -> "+analizePugin.pluginName+" over "+apkFile+"\n")
        pluginResult = analizePugin.main('-f',apkFile)
        results.append(Results(analizePugin.pluginName, pluginResult))
        print ("\n Finished: " + analizePugin.pluginName +" \n")
        print ("\n Starting CATEGORIZE! \n")
        categorize()

def storeResults():
    if (results):
        total = 0
        print("\n Storing Results over database")
        for result in results:
            db.insert_results(md5Id, result.plugin, 'location', '1', 'details', result.jsonResult, apkFile, username)
            total = total + 1
        print("\n DONE inserting into database \n")

def storeCategorized():
    if (categorizedResults):
        db.insert_results(md5Id, 'Categorized!', 'location', '1', 'details', json.dumps(categorizedResults, indent=4, sort_keys=True, default=str), apkFile, username)

def categorize():
    if (results):
        for result in results:
            with open(dictionaryOWASP, 'r') as d:
                owaspDict = json.load(d)

            resultDict = ast.literal_eval(result.jsonResult)
            flattenResultDict = flatten_dict(resultDict)
            resultValues = flattenResultDict.values()
            for vulnerability in resultValues:
                try:
                    if (type(vulnerability) == str and owaspDict[vulnerability]):
                        print("Found this vulnerability: "+ vulnerability)
                        toAdd =  [{
                                'name': vulnerability,
                                'details': owaspDict[vulnerability]['title'],
                                'severity': owaspDict[vulnerability]['level'],
                                'detectedby': result.plugin,
                                'feedback': [{ "url": owaspDict[vulnerability]['link']},
                                            {"video": owaspDict[vulnerability]['book']},
                                            {"book": owaspDict[vulnerability]['video']},
                                            {"other": "Nothing to show"}]
                        }]
                        categorizedResults[owaspDict[vulnerability]['category']].extend(toAdd)
                except KeyError:
                    pass

            print("\n "+result.plugin+" Categorized!")  

'''
A tool to scan APKs and look for vulnerabilities
'''
if __name__=="__main__":
    VERSION = '0.1'
    banner = "SCANNER PYTHON 3 PLUGINS"

    thisPlugin = 0

    print("\n"+str(banner)+"\n")

    text = "Tool that scans APKs and looks for vulnerabilities"
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument('-v', '--version', action='version', version='Vulnerability Scan Manager ' + VERSION)
    parser.add_argument('-f', '--file', help='The APK file to analyse.', action='store', dest='apkfile', nargs=1, default='')
    parser.add_argument('-m', '--md5', help='The APK file MD5 id to analyse.', action='store', dest='md5Id', nargs=1, default='')
    parser.add_argument('-u', '--user', help='User that upload the apk', action='store', dest='username', nargs=1, default='test')                    
    args = parser.parse_args()

    # print(args)

    apkFile = args.apkfile[0]
    md5Id = args.md5Id[0]
    username = args.username[0]

    print("\nAPK FILE -> " + apkFile)
    print("APK MD5 -> " + md5Id)
    print("Username -> " + username)
    print("\n")

    # looking for the plugins
    pluginDir = os.path.dirname(os.path.abspath(__file__)) # main plugin folder
    # completePluginDir = os.path.join(pluginDir, 'plugins3')

    print("Plugin folder -> " + pluginDir)

    # test the existence of the results directory
    if not os.path.exists(jsonResultsLocation):
        os.mkdir(jsonResultsLocation)
    
    counter_plugins = 0
    plugins = []
    results = []
    categorizedResults = {'M1':[],'M2':[],'M3':[],'M4':[],'M5':[],'M6':[],'M7':[],'M8':[],'M9':[],'M10':[]}

    for file in os.listdir(pluginDir):
        if file[0:8] == "plugin3_" and file[-3:] == ".py":
            print("file:"+file)
            module_name = "plugin3.".join(file.split(".")[0:-1])
            print("Importing -> " + module_name)
            # complete_path = os.path.join(completePluginDir, module_name)
            thisPlugin = __import__(module_name)
            # thisPlugin = imp.load_source(module_name, complete_path)
            plugins.append(thisPlugin)
            counter_plugins = counter_plugins + 1

    sys.argv = [sys.argv[0]]

    if (plugins):
        listPlugins()
        runPlugins()
        storeResults()
        storeCategorized()
