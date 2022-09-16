import collections
from datetime import datetime
import json
import subprocess
from typing import List, Union
from DataModel.Twitter.author import Author
from DataModel.Twitter.tweet import Tweet, TweetEncoder
from DataModel.Twitter.reaction import Reaction
import ast


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

    @staticmethod
    def getMediaUrl(media: dict):
        # print(len(media))
        if not media:
            return None
        else:
            for s_media in media:

                if 'Video' in s_media['_type']:
                    max_bit = None
                    for var in s_media['variants']:
                        max_bit = max_bit if max_bit is not None and var['bitrate'] is not None and \
                                             max_bit > var['bitrate'] else var['bitrate']
                        print(var['bitrate'], max_bit)

    def profile_scrape(self):
        subprocess.check_output(
            f'snscrape -n {self.max_results} --jsonl twitter-user {self.profileStr} >./Service/Twitter/twit_scrape.txt',
            shell=True)
        results = self.strToJSON()

        tweets: List[Tweet] = []
        for res in results:
            #self.getMediaUrl(res['media'])
            tweet = Tweet(res['id'],
                          self.getAuthorInfo(res['user']),
                          res['content'],
                          res['media'],
                          Reaction(res['likeCount'],
                                   res['replyCount'],
                                   res['retweetCount'],
                                   res['quoteCount']))

            tweets.append(tweet)

        JSONTweetsList = [TweetEncoder().default(tw) for tw in tweets]
        print(JSONTweetsList)

    # TODO implementare lo scraping di hashtag
    def hashtag(self):
        subprocess.check_output(
            f'snscrape -n {self.max_results} --jsonl twitter-hashtag {self.hashtagStr} >./Service/Twitter/twit_scrape.txt',
            shell=True)
        results = self.strToJSON()

        print(results)
