from searchAPIHarvester import TweetProcessor
from configs import configs
from streamAPIHarvester import TweetStreamProcessor
import couchdb
import sys

if len(sys.argv) == 2 and sys.argv[1] == '-h':
    print("Insert: python3 Main.py <ip> <port> <database> <user> <password> <file> <stream_id> <begin_id>(optional)")
    sys.exit()

ip = sys.argv[1]
port = sys.argv[2]
database = sys.argv[3]
user = sys.argv[4]
password = sys.argv[5]
file = sys.argv[6]
stream_id = int(sys.argv[7])
begin_id = int(sys.argv[8])

server = couchdb.Server("http://" + user + ":" + password + "@" + ip + ":" + port + "/")
if database in server:
    db = server[database]
else:
    db = server.create(database)
conf = configs[stream_id]

print('Database connected.')

thread_tweetPrc = TweetProcessor(conf['consumer_key'], conf['consumer_secret'], conf['access_token'],
                                 conf['access_token_secret'], conf['twitter-geo-latlngrad'], str(stream_id), db, begin_id)
thread_tweetstreamPrc = TweetStreamProcessor(conf['consumer_key'], conf['consumer_secret'],
                                             conf['access_token'], conf['access_token_secret'], conf['twitter-geo-rec'], str(stream_id), db)
print('Processor created.')
print('StreamProcessor created.')

# Running two threads at the same time
thread_tweetstreamPrc.start()
thread_tweetPrc.start()
