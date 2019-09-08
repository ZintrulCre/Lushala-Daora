import sys

sys.path.append('./')
import time
import json
from mpi4py import MPI
from collections import Counter
from Grid import Grid


def InitCounterAndDict():
    """
    Initialize the counters for zone tweets counting
    and hashtag counting
    """
    zone_count = Counter()
    hashtag_count = {}
    for zone in grid.zones:
        hashtag_count[zone] = Counter()
    hashtag_count['Other'] = Counter()
    return (zone_count, hashtag_count)


def HandleTweets(zone_range, tweet_strings):
    tweets = []
    for string in tweet_strings:
        # Preprocessing the lines read-in
        if "id" not in string:
            continue
        hashtags = []
        data = json.loads(string.strip(",\n"))
        text = data['doc']['text']
        while (True):
            # Extract the hashtag with string matching
            start = text.find(' #')
            end = text.find(' ', start + 2)
            if start == -1 or end == -1 or end == start + 2:
                break
            hashtags.append(text[start + 2:end].lower())
            text = text[end:]
            
        # Three possible approaches to extract the coordinates
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
            tweets.append({'x': 0, 'y': 0, 'hashtags': hashtags})
            continue
        # Store the coordinates and hashtags of each tweet
        tweets.append({'x': float(x), 'y': float(y), 'hashtags': hashtags})
    return tweets


def CountByBox(tweets, zones) -> tuple:
    """
    Initialize and update Counters for each bundle of tweets
    """
    zone_count, hashtag_count = InitCounterAndDict()
    for tweet in tweets:
        x = tweet['x']
        y = tweet['y']
        in_melb = False
        for zone, zone_range in zones.items():
            if x >= zone_range['x0'] and x <= zone_range['x1'] and y >= zone_range['y0'] and y <= zone_range['y1']:
                # If the coordinate of the tweet is within this zone
                in_melb = True
                zone_count[zone] += 1
                for hashtag in tweet['hashtags']:
                    hashtag_count[zone][hashtag] += 1
                break
        if not in_melb:
            # If the coordinates of the tweet is not within the given zones
            zone_count['Other'] += 1
            # Consider the tweet was sent from 'Other' area
            for hashtag in tweet['hashtags']:
                hashtag_count['Other'][hashtag] += 1
    return (zone_count, hashtag_count)


def UpdateCounterAndDict(zone_counts, hashtag_counts, zone_count, hashtag_count):
    """
    Update the Counters of the total result by sum up the
    Counters for each bundle of tweets
    """
    zone_counts += zone_count
    for zone in zones:
        hashtag_counts[zone] += hashtag_count[zone]
    hashtag_counts['Other'] += hashtag_count['Other']


def SumUp(num_process: int, result: list):
    """
    Sum up all the results from worker processes
    """
    zone_counts, hashtag_counts = InitCounterAndDict()
    for i in range(num_process):
        UpdateCounterAndDict(zone_counts, hashtag_counts, result[i][0], result[i][1])
    PrintResult(zone_counts, hashtag_counts)


def PrintResult(zone_counts, hashtag_counts):
    """
    Output the result
    """
    print("#tweets grouped by zone:")
    zone_counts = zone_counts.most_common()
    for zone in zone_counts:
        print("    - " + str(zone[0]) + ': ' + str(zone[1]) + ' posts')

    print("#hashtags grouped by zone:")
    for i in range(len(zone_counts)):
        zone = zone_counts[i]
        print("    - " + str(zone[0]) + ': ', hashtag_counts[zone[0]].most_common(5))


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    grid = Grid()
    zones = grid.zones

    if rank == 0:
        """
        The rank 0 process takes the responsibility of reading the fil and sum up 
        the results from all other process after finishing the processing part
        """
        print("------2 nodes and 8 cores MultiNode------")
        start_time = time.time()
        current_time = start_time

        i, num_subprocess = 1, 7
        file_name = "../bigTwitter.json"
        data = []
        with open(file_name, encoding="utf-8") as file:
            for line in file:
                data.append(line)
                if len(data) == 100:
                    # Send the tweets to a process after reading each 100 lines
                    comm.send(data, dest=i, tag=i)
                    i = 1 if i == num_subprocess else i + 1
                    data = []
            if len(data):
                # Send the remaining buffered lines
                comm.send(data, dest=i, tag=i)

        for i in range(1, num_subprocess + 1):
            comm.send(None, dest=i, tag=i)

        result = []
        for i in range(1, num_subprocess + 1):
            result.append(comm.recv(source=i, tag=0))
        SumUp(num_subprocess, result)

        end_time = time.time()
        print("total time:", end_time - start_time)
    else:
        """
        The process with other rank value takes the responsibility of process the 
        raw tweets and update the counters. After finished processing all tweets,
        the result will be returned to the process with rank 0.
        """
        zone_counts, hashtag_counts = InitCounterAndDict()
        while True:
            data = comm.recv(source=0, tag=rank)
            if data is None:
                break
            tweets = HandleTweets(grid.zone_range, data)
            zone_count, hashtag_count = CountByBox(tweets, zones)
            UpdateCounterAndDict(zone_counts, hashtag_counts, zone_count, hashtag_count)

        comm.send((zone_counts, hashtag_counts), dest=0, tag=0)
