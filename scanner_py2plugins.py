# vulnScanManager, will be responsible for checking a specific directory for apks and for processing them!
# -*- coding: UTF-8 -*-
from __future__ import absolute_import
import os.path
import argparse
import ConfigParser
# import imp
# import pkgutil
# import types
import sys
# import pkgutil
import database2 as db

config = ConfigParser.ConfigParser()
config.read('config.ini')

jsonResultsLocation = config.get('SCANNER', 'jsonResultsLocation')
apkDownloadedFolder = config.get('DOWNLOAD', 'apkDownloadDir')

class Results(object):
    def __init__(self, plugin=None, jsonResult=None):
        self.plugin = plugin
        self.jsonResult = jsonResult

def listPlugins():
    print("These are the available plugins:")
    for m in plugins:
        print("\n"+m.pluginName+"\n")


def runPlugins():
    print("Running all the available plugins:")
    for analizePugin in plugins:
        print ("\n Executing -> "+analizePugin.pluginName+" over "+apkFile+"\n")
        pluginResult = analizePugin.main(apkFile)
        # results.append(Results(analizePugin.pluginName, pluginResult))
        print (pluginResult)
        # c = analizePugin.PluginClass()
        # c.run(apkLocation)

# def selectPlugin(pluginNum):
#     thisPlugin = plugins[pluginNum]

def storeResults():
    if (results):
        total = 0
        print("\n Storing Results over database")
        for result in results:
            db.insert_results(md5Id, result.plugin, 'location', 'done', result.jsonResult, apkFile)
            total = total + 1
        print("\n DONE inserting into database, total: "+total)

# def runSelectedPlugin():
#     if thisPlugin == 0:
#         raise ValueError("you didn't assign a module yet.")
#     c = thisPlugin.PluginClass()
#     c.run()


# def run_this_plugin(plugin_number, apk_location, apk_md5):
#     thisPlugin = plugins[plugin_number]
#     c = thisPlugin.PluginClass()
#     c.run(apk_location, apk_md5)


'''
A tool to scan APKs and look for vulnerabilities
'''
if __name__=="__main__":
    VERSION = '0.1'
    banner = "SCANNER PYTHON 2 PLUGINS"

    thisPlugin = 0

    print("\n"+str(banner)+"\n")

    text = "Tool that scans APKs and looks for vulnerabilities"
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument('-v', '--version', action='version', version='Vulnerability Scan Manager ' + VERSION)
    parser.add_argument('-f', '--file', help='The APK file to analyse.',
                        action='store', dest='apkfile', nargs=1, default='')
    parser.add_argument('-m', '--md5', help='The APK file MD5 id to analyse.',
                        action='store', dest='md5Id', nargs=1, default='')
    args = parser.parse_args()

    # print(args)

    apkFile = args.apkfile[0]
    md5Id = args.md5Id[0]

    print("APK FILE -> " + apkFile)
    print("APK MD5 -> " + md5Id)

    # looking for the plugins
    pluginDir = os.path.dirname(os.path.abspath(__file__)) # main plugin folder
    # completePluginDir = os.path.join(pluginDir, 'plugins2')

    print("Plugin folder -> " + pluginDir)

    # test the existence of the results directory
    if not os.path.exists(jsonResultsLocation):
        os.mkdir(jsonResultsLocation)
    
    counter_plugins = 0
    plugins = []
    results = []

    for file in os.listdir(pluginDir):
        if file[0:8] == "plugin2_" and file[-3:] == ".py":
            print("file:"+file)
            module_name = "plugin2.".join(file.split(".")[0:-1])
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

    # an alternative testing to run the tools in parallel
    # for i in range(counter_plugins):
    #     jobs = []
    #     p = multiprocessing.Process(target=run_this_plugin, args=(i, apkFile, md5Id))
    #     jobs.append(p)
    #     p.start()

    # Execute plugins one by one (»TO DO: enroll into one function THEN multithreading )
    # print (plugins[1])
    # print (androbugs.main('-f', apkFile)) # plugins[plugin_number]

