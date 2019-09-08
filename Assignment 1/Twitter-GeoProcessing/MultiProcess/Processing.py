import json
from collections import Counter


def SplitTweetStrings(num_process:int, batch_size, zone_range, tweet_strings):
    tweet_string_batches = []
    for i in range(num_process):
        if i == num_process - 1:
            tweet_list = tweet_strings[i * batch_size:]
        else:
            tweet_list = tweet_strings[i * batch_size:i * batch_size + batch_size]
        tweet_string_batches.append((zone_range, tweet_list))
    return tweet_string_batches


def SplitTweets(num_process, batch_size, zones, tweets):
    tweet_batches = []
    for i in range(num_process):
        if i == num_process - 1:
            tweet_batch = tweets[i * batch_size:]
        else:
            tweet_batch = tweets[i * batch_size:i * batch_size + batch_size]
        tweet_batches.append((zones, tweet_batch))
    return tweet_batches


def HandleTweetStrings(input_tuple: tuple):
    zone_range = input_tuple[0]
    tweet_list = input_tuple[1]
    tweets = []
    for tweet in tweet_list:
        x = tweet['value']['geometry']['coordinates'][0]
        y = tweet['value']['geometry']['coordinates'][1]
        if x <= zone_range['max_x'] and x >= zone_range['min_x'] and y <= zone_range['max_y'] and y >= zone_range['min_y']:
                tweets.append({'x': x, 'y': y, 'tag': tweet['doc']['entities']['hashtags']})
    return tweets


def CountByBox(input_tuple) -> tuple:
    zones = input_tuple[0]
    tweets = input_tuple[1]
    zone_count = Counter()
    hashtag_count = {}
    for zone in zones:
        hashtag_count[zone] = Counter()
    for tweet in tweets:
        x = tweet['x']
        y = tweet['y']
        text = tweet['text']
        for zone, zone_range in zones.items():
            if x > zone_range['x0'] and x <= zone_range['x1'] and y > zone_range['y0'] and y <= zone_range['y1']:
                zone_count[zone] += 1
                hashtags = ExtractHashTag(text)
                for hashtag in hashtags:
                    hashtag_count[zone][hashtag] += 1
                break
    return zone_count, hashtag_count


def ExtractHashTag(text: str):
    res = []
    while True:
        start = text.find('#')
        if start == -1:
            break
        end = text.find(' ', start)
        res.append(text[start:end] if end != -1 else text[start:])
        text = text[end:]
    return res

def StatisticOutput(num_process: int, zones: dict, result: list):
    zone_count = Counter()
    hashtag_count = {}
    for zone in zones:
        hashtag_count[zone] = Counter()
    for i in range(num_process):
        zones = result[i][0]
        hashtags = result[i][1]
        zone_count += zones
        for zone in zones:
            hashtag_count[zone] += hashtags[zone]

    print("#tweets grouped by zone:")
    zone_count = zone_count.most_common()
    for zone in zone_count:
        print("    - " + str(zone[0]) + ':', zone[1])

    print("#hashtags grouped by zone:")
    for i in range(5):
        zone = zone_count[i]
        print("    - " + str(zone[0]) + ': ', hashtag_count[zone[0]].most_common(5))
