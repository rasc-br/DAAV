# vulnScanManager, will be responsible for checking a specific directory for apks and for processing them!
from __future__ import absolute_import
import os.path
import argparse
import configparser
import imp

config = configparser.ConfigParser()
config.read('config.ini')

# location of the results of the tool
jsonResultsLocation = config['SCANNER']['jsonResultsLocation']
# location of the unprocessed APKs
# apkDir = "/Users/cserrao/Documents/Development/AppSentinel/apks/unprocessed/"

def listPlugins():
    print("These are the available plugins:")
    for m in plugins:
        print("\n"+m.pluginName+"\n")


def runPlugins(apkLocation):
    print("Running all the available plugins:")
    for m in plugins:
        c = m.PluginClass()
        c.run(apkLocation)


def selectPlugin(pluginNum):
    thisPlugin = plugins[pluginNum]


def runSelectedPlugin():
    if thisPlugin == 0:
        raise ValueError("you didn't assign a module yet.")
    c = thisPlugin.PluginClass()
    c.run()


def run_this_plugin(plugin_number, apk_location, apk_md5):
    thisPlugin = plugins[plugin_number]
    c = thisPlugin.PluginClass()
    c.run(apk_location, apk_md5)


'''
A tool to scan APKs and look for vulnerabilities
'''
if __name__=="__main__":
    VERSION = '0.1'
    banner = "SCANNER PYTHON 3 PLUGINS"

    plugins = []
    thisPlugin = 0
    counter_plugins = 0

    print("\n"+str(banner)+"\n")

    text = "Tool that scans APKs and looks for vulnerabilities"
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument('-v', '--version', action='version', version='Vulnerability Scan Manager ' + VERSION)
    parser.add_argument('-f', '--file', help='The APK file to analyse.',
                        action='store', dest='apkfile', nargs=1, default='')
    parser.add_argument('-m', '--md5', help='The APK file MD5 id to analyse.',
                        action='store', dest='md5Id', nargs=1, default='')
    args = parser.parse_args()

    print(args)

    apkFile = args.apkfile[0]
    md5Id = args.md5Id[0]

    print("APK FILE -> " + apkFile)
    print("APK MD5 -> " + md5Id)

    # looking for the plugins
    pluginDir = os.path.dirname(os.path.abspath(__file__)) # main plugin folder
    completePluginDir = os.path.join(pluginDir, 'plugins3')
    print("Plugin folder -> " + completePluginDir)

    # test the existence of the results directory
    if not os.path.exists(jsonResultsLocation):
        os.mkdir(jsonResultsLocation)
    counter_plugins = 0
    plugins = []
    for file in os.listdir(completePluginDir):
        if file[0:7] == "plugin_" and file[-3:] == ".py":
            print("\n"+file)
            module_name = "plugin.".join(file.split(".")[0:-1])+".py"
            print("Importing -> " + module_name)
            complete_path = os.path.join(completePluginDir, module_name)
            # TODO: Used deprecated imp.load_source to dynamically found folder and file (python3)
            thisPlugin = imp.load_source(module_name, complete_path)
            plugins.append(thisPlugin)
            counter_plugins = counter_plugins + 1

    # we use the same approach to look for the APKs to analyse
    listPlugins()

    # this version runs the plugins concurrently
    # runPlugins(apkDir)

    # an alternative testing to run the tools in parallel
    # for i in range(counter_plugins):
    #     jobs = []
    #     p = multiprocessing.Process(target=run_this_plugin, args=(i, apkFile, md5Id))
    #     jobs.append(p)
    #     p.start()

    # Execute plugins one by one (»TO DO: enroll into one function THEN multithreading )

    # print (plugins[1])

    # to run androbugs it must be py -2
    # print (androbugs.main('-f', apkFile)) # plugins[plugin_number]

