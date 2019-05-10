import sys

if len(sys.argv) == 2 and sys.argv[1] == '-h':
    print("python3 Main.py <ip> <port> <database> <user> <password> <config_id>(config.py) <begin_id>(optional)")
    sys.exit()
elif len(sys.argv) != 7 or len(sys.argv) != 8:
    print("Wrong parameters!")
    print("Input -h for help.")

import os
import couchdb
from configs import configs
from searchAPIHarvester import TweetProcessor
from streamAPIHarvester import TweetStreamProcessor
os.system("sudo apt install python-pip")
os.system("sudo apt install python3-pip")
os.system("pip install --upgrade pip")
os.system("pip3 install --upgrade pip")
os.system("sudo pip install -r requirements.txt")
os.system("sudo pip3 install -r requirements.txt")

ip = sys.argv[1]
port = sys.argv[2]
database = sys.argv[3]
user = sys.argv[4]
password = sys.argv[5]
config_id = int(sys.argv[6])
if len(sys.argv) == 8:
    begin_id = int(sys.argv[7])
else:
    begin_id = None

server = couchdb.Server("http://" + user + ":" + password + "@" + ip + ":" + port + "/")
if database in server:
    db = server[database]
else:
    db = server.create(database)
conf = configs[config_id]

print('Database connected.')

thread_tweetPrc = TweetProcessor(conf['consumer_key'], conf['consumer_secret'], conf['access_token'],
                                 conf['access_token_secret'], conf['twitter-geo-latlngrad'], str(config_id), db, begin_id)
thread_tweetstreamPrc = TweetStreamProcessor(conf['consumer_key'], conf['consumer_secret'],
                                             conf['access_token'], conf['access_token_secret'], conf['twitter-geo-rec'], str(config_id), db)
print('Processor created.')
print('StreamProcessor created.')

# Running two threads at the same time
thread_tweetstreamPrc.start()
thread_tweetPrc.start()

print("Streaming. Enter ctrl + z to exit.")