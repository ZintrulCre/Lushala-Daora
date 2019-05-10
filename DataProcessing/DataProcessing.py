import os
import sys

if len(sys.argv) == 2 and sys.argv[1] == '-h':
    print("python3 FileToCouchdb.py <ip> <port> <database> <user> <password> <file>")
    sys.exit()
elif len(sys.argv) == 7:
    os.system("sudo apt install python-pip")
    os.system("sudo apt install python3-pip")
    os.system("sudo pip install couchdb")
    os.system("sudo pip3 install couchdb")
    import couchdb
    import json
    import time
    from TextAnalysis import GreedAnalysis

    greedy_analysis = GreedAnalysis()

    ip = sys.argv[1]
    port = sys.argv[2]
    database = sys.argv[3]
    user = sys.argv[4]
    password = sys.argv[5]
    file = sys.argv[6]
    server = couchdb.Server("http://" + user + ":" + password + "@" + ip + ":" + port + "/")
    if database in server:
        db = server[database]
    else:
        db = server.create(database)

    with open(file) as file:
        file.readline()
        for line in file:
            if line[0] == ']':
                break
            line = line.strip().strip(',')
            content = json.loads(line)
            if not content['doc']['coordinates']:
                continue
            text = content['doc']['text']
            coordinates = None if not content['doc']['coordinates'] else content['doc']['coordinates']['coordinates']
            user = {}
            user['id'] = content['doc']['user']['id_str']
            user['name'] = content['doc']['user']['name']
            user['location'] = content['doc']['user']['location']
            user['description'] = content['doc']['user']['description']
            time = content['doc']['created_at']

            greedy = greedy_analysis.Analyze(text)

            doc_id, doc_rev = db.save({'text': text, 'coordinates': coordinates, 'user': user, 'time': time, 'greedy': greedy})
            print(doc_id, doc_rev)
else:
    print("Wrong arguments!")
    sys.exit()
