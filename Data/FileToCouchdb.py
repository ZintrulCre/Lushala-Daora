import os
import sys
import json
import time

if len(sys.argv) == 2 and sys.argv[1] == '-h':
    print("Insert: python3 FileToCouchdb.py <ip> <port> <database> <user> <password> <file>")
    # print("Query: python3 FileToCouchdb.py -q")
    # print("Retrive: python3 FileToCouchdb.py -r <id>")
    sys.exit()
elif len(sys.argv) == 7:
    os.system("pip install couchdb")
    import couchdb

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
            text = content['doc']['text']
            doc_id, doc_rev = db.save({'text': text})
            print(doc_id, doc_rev)
else:
    print("Wrong arguments!")
    sys.exit()
