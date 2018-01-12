import getopt
import re  # regexp
import sys  # open file
import requests
import json

try:
    options,files=getopt.getopt(sys.argv[1:], 'i:', ['index='])
except getopt.GetoptError as err:
    print("./logToElastic.py --index={1} [files]")
    sys.exit(1)

index=None
for opt, arg in options:
    if opt in ('-i', '--index'):
        index=arg
if index is None:
    print("./logToElastic.py --index={1} [files]")
    sys.exit(1)
mtype="logs"

url='http://spirana.lille.inria.fr/'
url_index='{}{}/'.format(url, index)
url_type='{}{}/'.format(url_index,mtype)
headers={'Content-Type': 'application/json'}

# check mapping
# curl -XGET 'http://spirana.lille.inria.fr/chat2/_mapping/logs' | python -m json.tool

# removes index
# curl -XDELETE 'http://spirana.lille.inria.fr/{}/'.format(index)

# creating index and mapping

mapping = {
    "mappings": {
        mtype: {
            "properties": {
	        "timestamp": {
                    "type":   "date",
	            "format": "yyyy.MM.dd-HH.mm.ss.SSS"
	        }
            }
        }
    }
}
print(requests.put(url_index, data=json.dumps(mapping), headers=headers).text)


logRegexp = "(^[^ ]*) ([^ ]*) (.*)"
parser = re.compile(logRegexp)

for mfile in files:
    with open(mfile, 'r') as f:
        for line in f:
            r = parser.match(line)
            data = {"message": r.group(3),
                    "timestamp": r.group(1),
                    "agent": r.group(2)}
            print(data)
            print(requests.post(url_type, data=json.dumps(data), headers=headers).text)
