import os
import json
os.system("pip install requests")
import requests

with open('Data/test.json') as file:
    file.readline()
    id = 1
    for line in file:
        if line[0] == ']':
            break
        line = line.strip().strip(',')
        content = json.loads(line)
        text = content['doc']['text']
        data = {}
        data['id'] = str(id)
        data['text'] = text
        data = json.dumps(data)
        # print(data)
        response = requests.put("http://172.26.37.212:5984/melb/" + str(id), data=data)
        print(response.text)
        # command = "curl -u admin:password -X PUT http://172.26.37.212:5984/melbourne_db/" + str(id) + " -d '" + data + "'"
        # print(command)
        # os.system(command)
        id += 1
