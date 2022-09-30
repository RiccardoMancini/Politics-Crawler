import collections
from datetime import datetime, timedelta, date
import json
import subprocess
from typing import List, Union, Iterable

from pymongo.database import Database

from DataModel.Twitter.author import Author
from DataModel.Twitter.tweet import Tweet, TweetEncoder
from DataModel.Twitter.reaction import Reaction
from pymongo import MongoClient
from snscrape.modules.twitter import TwitterSearchScraper


class TwitterScrape:

    def __init__(self, profile: str = "", hashtag: str = "", keyword: str = "", max_results: int = 100,
                 since: date = None, until: date = None):
        self.profileStr = profile
        self.hashtagStr = hashtag
        self.keyword = keyword
        self.max_results = max_results
        self.since = since if since is not None else datetime.now().date() - timedelta(days=1)
        self.until = until if until is not None else datetime.now().date()

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
        if not media:
            return None
        else:
            # print(media)
            if len(media) < 2:
                s_media = media[0]
                if 'Video' in s_media['_type']:
                    max_bit = None
                    for var in s_media['variants']:
                        if var['bitrate'] is None:
                            continue
                        max_bit = max_bit if max_bit is not None and max_bit > var['bitrate'] else var['bitrate']
                        # print(var['bitrate'], max_bit)
                    videoObj = [flt for flt in filter(lambda x: x['bitrate'] == max_bit, s_media['variants'])]
                    # print(videoObj[0]['url'], videoObj[0]['bitrate'])
                    return [videoObj[0]['url']]
                if 'Gif' in s_media['_type']:
                    return [s_media['variants'][0]['url']]
                else:
                    return [s_media['fullUrl']]
            else:
                return [s_media['fullUrl'] for s_media in media]

    @staticmethod
    def avgReaction(reaction: any) -> float:
        return (reaction["n_like"] + reaction["n_retweet"] + reaction["n_reply"] + reaction["n_quote"]) / 4

    def getListOfTweets(self, results: Iterable) -> List[dict]:
        tweets: List[Tweet] = []
        for res in results:
            # print(self.getMediaUrl(res['media']))
            tweet = Tweet(res['id'],
                          self.getAuthorInfo(res['user']),
                          res['content'],
                          self.getMediaUrl(res['media']),
                          Reaction(res['likeCount'],
                                   res['replyCount'],
                                   res['retweetCount'],
                                   res['quoteCount']),
                          [self.keyword])
            tweets.append(tweet)

        return [TweetEncoder().default(tw) for tw in tweets]

    @staticmethod
    def encodeStr(*args):
        argsCoded = []
        for text in args:
            argsCoded.append(text.encode(encoding='UTF-8', errors='ignore'))
        return argsCoded

    def keyword_scrape(self, db: Database) -> None:
        subprocess.check_output(
            f'snscrape -n {self.max_results} --jsonl --progress twitter-search "{self.keyword} '
            f'since:{self.since} until:{self.until}" >'
            f'./Service/Twitter/twit_scrape.txt',
            shell=True)
        results: Iterable = self.strToJSON()

        JSONTweetsList: List[dict] = self.getListOfTweets(results)
        #print(JSONTweetsList)

        for tw in JSONTweetsList:
            tweetEx = db.tweets.find_one({"_id": tw['tweet_id']})
            if tweetEx is None:
                db_tweet = {"_id": tw['tweet_id']}
                del tw['tweet_id']
                tw['text'], tw['keyword'][0], tw['author']['username'], tw['author']['desc'] = \
                    self.encodeStr(tw['text'], tw['keyword'][0], tw['author']['username'], tw['author']['desc'])
                if tw['media_url'] is not None:
                    tw['media_url'] = [url.encode(encoding='UTF-8', errors='ignore') for url in tw['media_url']]

                author = db.authors.find_one({"_id": tw['author']['user_id']})
                if author is not None:
                    tw['author'] = author['_id']
                else:
                    tw_app = tw['author'].copy()
                    db_author = {"_id": tw_app['user_id']}
                    del tw_app['user_id']
                    db_author.update(tw_app)
                    db.authors.insert_one(db_author)
                    tw['author'] = tw['author']['user_id']

                db_tweet.update(tw)
                db.tweets.insert_one(db_tweet)
            else:
                new_keyword = self.encodeStr(tw['keyword'][0])[0]
                # print(new_keyword not in tweetEx['keyword'], new_keyword, tweetEx['keyword'])
                if new_keyword not in tweetEx['keyword']:
                    tweetEx['keyword'].append(new_keyword)
                    print(tweetEx)
                    db.tweets.save(tweetEx)

        # print(db.tweets.count(), db.authors.count())

        '''JSONTweetsList.sort(key=lambda x: self.avgReaction(x['reaction']), reverse=False)'''

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
