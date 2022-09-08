import collections
from datetime import datetime
import json
import subprocess
from typing import List
from DataModel.Twitter.author import Author
from DataModel.Twitter.tweet import Tweet, TweetEncoder
from DataModel.Twitter.reaction import Reaction


class TwitterScrape:

    def __init__(self, profile: str = "", hashtag: str = "", max_results: int = 100,
                 since: datetime = None, until: datetime = None):
        self.profileStr = profile
        self.hashtagStr = hashtag
        self.max_results = max_results
        self.since = since if since is not None else datetime.min
        self.until = until if until is not None else datetime.now()

    @staticmethod
    def strToJSON() -> collections.Iterable:
        new_lines = ''
        with open('./Service/Twitter/twit_scrape.txt') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                new_lines = line if i == 0 else new_lines + ',' + line
        return json.loads('[' + new_lines + ']')

    @staticmethod
    def getAuthorInfo(user: dict) -> Author:
        return Author(user['id'],
                      user['username'],
                      user['description'],
                      user['followersCount'],
                      user['friendsCount'],
                      user['statusesCount'],
                      user['favouritesCount'],
                      user['mediaCount'])

    def profile_scrape(self):
        subprocess.check_output(
            f'snscrape -n {self.max_results} --jsonl twitter-user {self.profileStr} >./Service/Twitter/twit_scrape.txt',
            shell=True)
        results = self.strToJSON()

        tweets: List[Tweet] = []
        for res in results:
            tweet = Tweet(res['id'],
                          self.getAuthorInfo(res['user']),
                          res['content'],
                          res['media'],
                          Reaction(res['likeCount'],
                                   res['replyCount'],
                                   res['retweetCount'],
                                   res['quoteCount']))

            tweets.append(tweet)

        JSONTweetsList = [TweetEncoder().encode(tw) for tw in tweets]

        print(JSONTweetsList)

    # TODO implementare lo scraping di hashtag
    # def hashtag(self):
