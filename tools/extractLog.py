import re  # regexp
import sys  # open file
import requests
import json


class AndroidLogEntry:

    def __init__(self, date, time, info, msg):
        self.date = date
        self.time = time
        self.info = info
        self.msg = msg


class NotFound(Exception):
    pass


class AndroidLogParser:
    # https://developer.android.com/studio/debug/am-logcat.html
    androidLogRegexp = "([0-9]{2}-[0-9]{2}) ([0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}) ([^:]*): (.*)"

    def __init__(self):
        self.parser = re.compile(AndroidLogParser.androidLogRegexp)  # prepare regexp

    def parseLine(self, line):
        r = self.parser.match(line)
        if r is None:
            raise NotFound()
        return AndroidLogEntry(date=r.group(1), time=r.group(2), info=r.group(3), msg=r.group(4))

    def parserLogFile(self, fileName):
        headers = {'Content-Type': 'application/json'}
        with open(fileName, 'r') as f:
            for line in f:
                try:
                    tokens = self.parseLine(line)
                    print("date: {0}\ttime: {1}\tinfo: {2}\tmsg: {3}".format(
                        tokens.date,
                        tokens.time,
                        tokens.info,
                        tokens.msg))
                    #data = {"MESSAGE": tokens.msg,
                    #        "timestamp": "2017-%sT%s" % (tokens.date, tokens.time)}
                    #print(requests.post('http://spirana.lille.inria.fr/custom1/logs/',
                    #                    data=json.dumps(data),
                    #                    headers=headers).text)
                except NotFound as inst:
                    print("couldNotParse {}".format(line[:-1]), file=sys.stderr)


if len(sys.argv) == 2:
    AndroidLogParser().parserLogFile(sys.argv[1])
else:
    print("You must specify a fileName")
