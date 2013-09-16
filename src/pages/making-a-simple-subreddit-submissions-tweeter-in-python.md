title: Making a simple subreddit submissions tweeter in Python  
published: 2013-09-16

In this short post we are going write a simple script in Python that reads
submissions from a subreddit and posts links to them on Twitter.

## Setup

First, create a `virtualenv` and activate it with:

    :::sh
    $ virtualenv -p /usr/bin/python2 env
    $ source env/bin/activate

Then install the necessary dependencies `tweepy` and `requests`:

    :::sh
    $ pip install tweepy requests

## Method for retrieving subreddit submissions

Using the library
[requests](http://docs.python-requests.org/en/latest/index.html) we will fetch
new submissions from a subreddit:

    :::python
    import requests
    def get_reddit_posts(subreddit, number_of_posts):
        reddit = requests.get('http://www.reddit.com/r/{}/new/.json?limit={}'
                                  .format(subreddit, number_of_posts),
                              headers={'User-Agent': 'Reddit Tweeter'})
        submissions = reddit.json()['data']['children']
        submissions = [{'id': s['data']['id'],
                        'title': s['data']['title'],
                        'url': 'http://redd.it/{}'.format(s['data']['id'])
                       } for s in submissions]
        return submissions

The method returns a list of dictionaries containing the submissions' IDs,
titles and URLs.

## Get a Twitter access token and consumer key

Visit [Twitter's dev page](https://dev.twitter.com/apps) and create a new app.
When you have created an app, visit its settings page and change `Access` to
`Read and Write`. Then go back to the `Details` view and create an access
token.

When that's done, go back to Python and create the following global variables
with your data:

    :::python
    ACCESS_TOKEN = ''
    ACCESS_TOKEN_SECRET = ''
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''

## Method for posting submissions to Twitter

Define the following global variables:

    :::python
    TAGS = '#Python #Programming'
    SUBREDDIT = 'python'
    NUMBER_OF_POSTS = 30

Of course are you free to change these values to anything you want.

Then write the following method:

    :::python
    import tweepy
    def tweet(submissions):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        for each in submissions:
            # Add the url and the tags to the tweet
            tweet = u'{} {}'.format(each['url'], TAGS)
            title_length = len(each['title'])
            title = None
            if title_length < 139 - len(tweet):
                # The whole title fits in the tweet
                title = each['title']
            else:
                # If the title doesn't fit, make it end with `...`
                title = u'{}...'.format(each['title'][:139 - len(tweet) - 4])
            tweet = u'{} {}'.format(title, tweet)
            print(u'[bot] posting: {}'.format(tweet))
            # Try to post the tweet
            try:
                api.update_status(tweet)
            except tweepy.TweepError, e:
                if e.message[0]['code'] == 187:
                    print('[bot] Tweet is a duplicate')
                    continue

* This method takes the list of submissions as an argument.
* Then it sets up access to Twitter's API.
* For each submission it will post a tweet.
    * First we set `tweet` to Reddit's short URL and the previously specified
      tags.
    * If the length of the title is shorter than the URL and the tags we can
      just prepend it to the tweet. Otherwise we cuts the title off and ends it
with `...`.
    * When the tweet is ready, post it to Twitter with
      `api.update_status(tweet)`.

## Main method

Lastly we will write the main method that binds the previously two methods
together:

    :::python
    if __name__ == '__main__':
        submissions = get_reddit_posts(SUBREDDIT, NUMBER_OF_POSTS)
        tweet(submissions)

## Complete script

<script src="https://gist.github.com/MaTachi/6584762.js"></script>

## Room for further improvements

This is just a very first version of something that could become a nice bot.
For example could the submission IDs be stored in a file or a SQLite database
to keep track of which submission that have already been tweeted. The global
variables could be moved to a separate .ini config file. We could use a proper
logger. And we could also set up a cronjob to automatically post new tweets
regularly.

## Inspiration

I wrote this post because of the inspiration I got from this [Reddit
discussion](http://www.reddit.com/r/Python/comments/1mdlq1/making_a_reddit_twitter_bot/)
about another Reddit + Twitter bot.
