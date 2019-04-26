# Plugin to handle the tools capable of setting the input for "DroidstatX" and handle the output
import os
import database as db
import configparser
import logging as log
import linecache

config = configparser.ConfigParser()
config.read('config.ini')

log.basicConfig(filename=config['GENERAL']['logDir'] + "appsentinel.log", filemode='a', format='%(asctime)s,%(msecs)d | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)

pluginName = "Androbugs"
enable = True

jsonResultsLocation = config['SCANNER']['jsonResultsLocation'] + "/" + pluginName + "/"
androbugsLocation = config['ANDROBUGS']['androbugsLocation']


class PluginClass:
    def __init__(self):
        ''' constructor '''

    def convert_to_json(self, md5):
        txt_file = open(jsonResultsLocation + md5 + ".txt", "r")
        lines = txt_file.readlines()
        line_counter = 1
        critical = []
        warning = []
        notice = []
        info = []

        critical_status = False
        warning_status = False
        notice_status = False
        info_status = False
        add = True
        for line in lines:
            if line.startswith("[Critical]"):
                critical.append("Critical")
                critical_status = True
                warning_status = False
                notice_status = False
                info_status = False
                add = True
            if line.startswith("[Warning]"):
                warning.append("Warning")
                critical_status = False
                warning_status = True
                notice_status = False
                info_status = False
                add = True
            if line.startswith("[Notice]"):
                notice.append("Notice")
                critical_status = False
                warning_status = False
                notice_status = True
                info_status = False
                add = True
            if line.startswith("[Info]"):
                info.append("Info")
                critical_status = False
                warning_status = False
                notice_status = False
                info_status = True
                add = True
            if line.startswith("-------"):
                add = False
            if critical_status and add:
                critical.append(line_counter)
            if warning_status and add:
                warning.append(line_counter)
            if notice_status and add:
                notice.append(line_counter)
            if info_status and add:
                info.append(line_counter)
            line_counter = line_counter + 1

        # print(critical)
        # print(warning)
        # print(notice)
        # print(info)

        # now let's try to put everything on a JSON format :-)
        json_file = open(jsonResultsLocation + md5 + ".json", "w")
        json_file.write("{")
        json_file.write("\"results\": ")
        json_file.write("{\"critical_level\": [")
        text2write = ""
        is_first = True
        for critical_line in critical:
            if critical_line == 'Critical' and is_first:
                text2write = text2write + "{\"critical\": \""
                is_first = False
                continue
            if critical_line == 'Critical' and not is_first:
                text2write = text2write + "\"}, {\"critical\": \""
            else:
                what2write = linecache.getline(jsonResultsLocation + md5 + ".txt", critical_line)
                text2write = text2write + what2write.replace('"', '\\"')[:-1]
        text2write = text2write + "\"}]"
        json_file.write(text2write)
        json_file.write(",")
        json_file.write("\"warning_level\": [")
        text2write = ""
        is_first = True
        for warning_line in warning:
            if warning_line == 'Warning' and is_first:
                text2write = text2write + "{\"warning\": \""
                is_first = False
                continue
            if warning_line == 'Warning' and not is_first:
                text2write = text2write + "\"}, {\"warning\": \""
            else:
                what2write = linecache.getline(jsonResultsLocation + md5 + ".txt", warning_line)
                text2write = text2write + what2write.replace('"', '\\"')[:-1]
        text2write = text2write + "\"}"
        json_file.write(text2write)
        json_file.write("],")
        json_file.write("\"notice_level\": [")
        text2write = ""
        is_first = True
        for notice_line in notice:
            if notice_line == 'Notice' and is_first:
                text2write = text2write + "{\"notice\": \""
                is_first = False
                continue
            if notice_line == 'Notice' and not is_first:
                text2write = text2write + "\"}, {\"notice\": \""
            else:
                what2write = linecache.getline(jsonResultsLocation + md5 + ".txt", notice_line)
                text2write = text2write + what2write.replace('"', '\\"')[:-1]
        text2write = text2write + "\"}"
        json_file.write(text2write)
        json_file.write("],")
        json_file.write("\"info_level\": [")
        text2write = ""
        is_first = True
        for info_line in info:
            if info_line == 'Info' and is_first:
                text2write = text2write + "{\"info\": \""
                is_first = False
                continue
            if info_line == 'Info' and not is_first:
                text2write = text2write + "\"}, {\"info\": \""
            else:
                what2write = linecache.getline(jsonResultsLocation + md5 + ".txt", info_line)
                text2write = text2write + what2write.replace('"', '\\"')[:-1]
        text2write = text2write + "\"}"
        json_file.write(text2write)
        json_file.write("]")
        json_file.write("}")
        json_file.write("}")

    def run(self, apk_file, md5):
        print(pluginName + ": Running the Androbugs plugin!...")
        log.debug(pluginName + ": Running the Androbugs plugin!...")
        # test the existence of the results directory
        if not os.path.exists(jsonResultsLocation):
            os.system("mkdir " + jsonResultsLocation)

        # don't know why, but Androbugs requires running from the APK dir
        # print("ANDROBUGS cd " + apkLocation)
        # os.system("cd " + apkLocation)
        if apk_file[-4:] == ".apk":
            print(pluginName + ": Running on -> " + apk_file)
            log.debug(pluginName + ": Running on -> " + apk_file)
            print(pluginName + ": Executing -> python2 " + androbugsLocation + "androbugs.py -f " + apk_file + " --md5file " + md5 + " -o " + jsonResultsLocation)
            log.debug(pluginName + ": Executing -> python2 " + androbugsLocation + "androbugs.py -f " + apk_file + " --md5file " + md5 + " -o " + jsonResultsLocation)
            # run the tool
            os.system("python2 " + androbugsLocation + "androbugs.py -v -f " + apk_file + " --md5file " + md5 +" -o " + jsonResultsLocation)
            # this tool produces a text-based output... we need to consider what to do with this
            # convert to JSON
            self.convert_to_json(md5)
            # have also the information registered on the database
            db.insert_results(md5, pluginName, jsonResultsLocation + md5 + ".json", 0, "NOT YET IN THE FINAL FORMAT")

