import re  # regexp
import sys  # open file
import requests
import json

url='http://spirana.lille.inria.fr/chat/logs/'
headers={'Content-Type': 'application/json'}

logRegexp = "(^[^ ]*) ([^ ]*) (.*)"
parser = re.compile(logRegexp)

with open(sys.argv[1], 'r') as f:
    for line in f:
        r = parser.match(line)
        data = {"message": r.group(3),
                "timestamp": r.group(1),
                "agent": r.group(2)}
        print(data)
        print(requests.post(url, data=json.dumps(data), headers=headers).text)
