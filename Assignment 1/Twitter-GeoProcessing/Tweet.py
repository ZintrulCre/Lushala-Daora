import matplotlib.pyplot as plt


class Tweet:
    def __init__(self, range):
        # todo: stream read
        tweet_file = "../tinyTwitter.json"
        with open(tweet_file, 'r') as tweet_file:
            self.tweet_strings = tweet_file.readlines()

    def Plot(self, grid_matrix, tweets):
        file = "Grid-and-Tweet.png"
        grid_x, grid_y = grid_matrix['x'], grid_matrix['y']
        x, y = [], []
        for dict in tweets:
            x.append(dict['x'])
            y.append(dict['y'])
        plt.figure('GridPoint')
        plt.plot(x, y, 'ro')
        plt.plot(grid_x, grid_y, 'bx')
        plt.draw()
        plt.savefig(file)
        plt.close()
