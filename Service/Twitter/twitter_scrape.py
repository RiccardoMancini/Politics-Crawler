import collections
import datetime
import json
import subprocess
from typing import List, Union

from pymongo.database import Database

from DataModel.Twitter.author import Author
from DataModel.Twitter.tweet import Tweet, TweetEncoder
from DataModel.Twitter.reaction import Reaction
from pymongo import MongoClient
from snscrape.modules.twitter import TwitterSearchScraper


class TwitterScrape:

    def __init__(self, profile: str = "", hashtag: str = "", keyword: str = "", max_results: int = 100,
                 since: datetime = None, until: datetime = None):
        self.profileStr = profile
        self.hashtagStr = hashtag
        self.keyword = keyword
        self.max_results = max_results
        self.since = since if since is not None else datetime.datetime.min
        self.until = until if until is not None else datetime.datetime.now()

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
                # TODO da finire l'estrazione di media

    @staticmethod
    def avgReaction(reaction: any) -> float:
        return (reaction["n_like"] + reaction["n_retweet"] + reaction["n_reply"] + reaction["n_quote"]) / 4

    def keyword_scrape(self, db: Database):
        subprocess.check_output(
            f'snscrape -n {self.max_results} --jsonl --progress twitter-search "{self.keyword} '
            f'since:{datetime.date(2022, 9, 26)}" >'
            f'./Service/Twitter/twit_scrape.txt',
            shell=True)
        results = self.strToJSON()

        # -------------------------------- jsonTweetsListBuild(results): Array<JSON>
        tweets: List[Tweet] = []
        for res in results:

            # self.getMediaUrl(res['media'])
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
        # --------------------------------

        print(JSONTweetsList)
        db.tweets.insert_many(JSONTweetsList)
        '''x['reaction']['n_like']'''
        '''JSONTweetsList.sort(key=lambda x: self.avgReaction(x['reaction']), reverse=False)
        return JSONTweetsList'''

        # filteredJSONTweetsList = [tw for tw in JSONTweetsList if tw["reaction"]["n_like"] > 10]

    # TODO implementare lo scraping di profili
    def profile_scrape(self):
        subprocess.check_output(
            f'snscrape -n {self.max_results} --jsonl twitter-user {self.profileStr} >./Service/Twitter/twit_scrape.txt',
            shell=True)
        results = self.strToJSON()

        tweets: List[Tweet] = []
        for res in results:
            # self.getMediaUrl(res['media'])
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
