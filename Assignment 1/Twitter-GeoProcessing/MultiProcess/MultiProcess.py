import time
from multiprocessing import Pool

from Grid import Grid
from Tweet import Tweet
from MultiProcess.Processing import *
from Processing import UpdateCurrentTimeAndOutput

print("------1 node and 8 cores multiprocess------")
print("------Initializing------")
start_time = time.time()
current_time = start_time

num_process = 8
pool = Pool(processes=num_process)

grid = Grid()
tweet = Tweet(grid.zone_range)
tweet_strings = tweet.tweet_strings
total_num_tweets = len(tweet_strings)

current_time = UpdateCurrentTimeAndOutput(current_time)

print("------Preprocessing------")
batch_size = total_num_tweets // num_process
tweet_string_batches = SplitTweetStrings(num_process, batch_size, grid.zone_range, tweet_strings)
result = pool.map(HandleTweetStrings, tweet_string_batches)

tweets = []
for i in range(num_process):
    tweets += result[i]

print("#tweets:", len(tweets))
current_time = UpdateCurrentTimeAndOutput(current_time)

# 1 node and 8 core
print("------Counting------")
batch_size = len(tweets) // num_process
tweet_batches = SplitTweets(num_process, batch_size, grid.zones, tweets)
result = pool.map(CountByBox, tweet_batches)
StatisticOutput(num_process, grid.zones, result)
current_time = UpdateCurrentTimeAndOutput(current_time)

end_time = time.time()
print("total time:", end_time - start_time, '\n')
