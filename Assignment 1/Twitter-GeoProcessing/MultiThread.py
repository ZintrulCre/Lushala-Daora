import sys

sys.path.append('./')
import json
import time
import threading
from queue import Queue
from collections import Counter

from Grid import Grid

def CountByBox(tweets, zone_count, hashtag_count, zones) -> tuple:
    
    for tweet in tweets:
        x = tweet['x']
        y = tweet['y']
        in_melb = False
        for zone, zone_range in zones.items():
            if x >= zone_range['x0'] and x <= zone_range['x1'] and y >= zone_range['y0'] and y <= zone_range['y1']:
            # If coordinates of the tweet are within this zone
                in_melb = True
                zone_count[zone] += 1
                for hashtag in tweet['hashtags']:
                    hashtag_count[zone][hashtag.lower()] += 1
                    # Update the counter of corresponding hashtag and zone
                break
        if not in_melb:
            zone_count['Other'] += 1
            # Consider this tweeter sending from other zones
            for hashtag in tweet['hashtags']:
                hashtag_count['Other'][hashtag] += 1
                # Update the counter of the hashtag in 'other' zone
    return (zone_count, hashtag_count)


def CountTweetsAndHashtags(num_thread: int, zones: dict, result: list):
    """
    Sum up the results from different threads and output the final statistics
    """
    
    zone_count = Counter()
    hashtag_count = {}
    for zone in zones:
        hashtag_count[zone] = Counter()
    hashtag_count['Other'] = Counter()
    # Initialize all counters for final statistics
    
    for i in range(num_thread):
        # Sum up results from all threads
        zones_counter = result[i][0]
        hashtags = result[i][1]
        zone_count += zones_counter
        for zone in zones:
            hashtag_count[zone] += hashtags[zone]
            
    # Output final results
    print("#tweets grouped by zone:")
    zone_count = zone_count.most_common()
    for zone in zone_count:
        print("    - " + str(zone[0]) + ': ' + str(zone[1]) + ' posts')

    print("#hashtags grouped by zone:")
    for i in range(len(zone_count)):
        zone = zone_count[i]
        print("    - " + str(zone[0]) + ': ', hashtag_count[zone[0]].most_common(5))


def worker():
    """
    The worker thread which takes the responsibiltiy of
    processing the tweets and updating the counter.
    The final results will be returned to the main thread
    after finished processing all the tweets.
    """
    zone_count = Counter()
    hashtag_count = {}
    for zone in zones:
        hashtag_count[zone] = Counter()
    hashtag_count['Other'] = Counter()
    #Initializing the counters
    while True:
        #Keep getting bundles of tweets from main thread
        item = q.get()
        if item is None:
            break
        CountByBox(item, zone_count, hashtag_count, zones) #Processing and updating the counter
        q.task_done()
    result.append([zone_count, hashtag_count]) #Return the final result


print("------1 node and 1 core multithread------")
# initialize
start_time = time.time()
current_time = start_time

grid = Grid()
zones = grid.zones

num_threads = 1
q = Queue()
t = threading.Thread(target=worker)
t.start()
result = []


file_name = "../bigTwitter.json"
json_list = []
with open(file_name, 'r', encoding='UTF-8') as file:
    for line in file:
        # Reading the file line by line
        if "id" not in line:
            continue
        line = line.strip(',\n')
        data = json.loads(line)
        
        # Preprocessing part 
        # Three possible ways of getting coordinates
        if data['value'] != 1:
            x = data['value']['geometry']['coordinates'][0]
            y = data['value']['geometry']['coordinates'][1]
        elif data['doc'] and data['doc']['coordinates'] and data['doc']['coordinates']['coordinates']:
            x = data['doc']['coordinates']['coordinates'][0]
            y = data['doc']['coordinates']['coordinates'][1]
        elif data['doc'] and data['doc']['geo'] and data['doc']['geo']['coordinates']:
            x = data['doc']['geo']['coordinates'][1]
            y = data['doc']['geo']['coordinates'][0]
        else:
            x = 0
            y = 0
        hashtags = []
        for hashtag in data['doc']['entities']['hashtags']:
            hashtags.append(hashtag['text'])
        tweet = {'x': x,'y': y,
                 'hashtags': hashtags}
        json_list.append(tweet)
        if len(json_list) == 100:
            # Put the list of tweets into the queue after reading each 100 lines
            # for worker threads to process
            q.put(json_list)
            json_list = []
    if len(json_list) != 0:
        # Put the remaining tweets into the queue
        q.put(json_list)
q.join()
q.put(None)
t.join()

# Sum up results from all worker threads and get the final statistics
CountTweetsAndHashtags(num_threads, grid.zones, result)

end_time = time.time()
print("total time:", end_time - start_time, '\n')
