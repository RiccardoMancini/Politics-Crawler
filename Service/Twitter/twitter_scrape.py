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
                # TODO gestire le gif
                else:
                    print(s_media)
                    return [s_media['fullUrl']]
            else:
                return [s_media['fullUrl'] for s_media in media]

    @staticmethod
    def avgReaction(reaction: any) -> float:
        return (reaction["n_like"] + reaction["n_retweet"] + reaction["n_reply"] + reaction["n_quote"]) / 4

    def keyword_scrape(self, db: Database):
        subprocess.check_output(
            f'snscrape -n {self.max_results} --jsonl --progress twitter-search "{self.keyword} '
            f'since:{datetime.date(2022, 9, 23)} until:{datetime.date(2022, 9, 25)}" >'
            f'./Service/Twitter/twit_scrape.txt',
            shell=True)
        results = self.strToJSON()

        # -------------------------------- jsonTweetsListBuild(results): Array<JSON>
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
                          self.keyword)
            tweets.append(tweet)

        JSONTweetsList = [TweetEncoder().default(tw) for tw in tweets]
        # --------------------------------

        print(JSONTweetsList)

        #db.tweets.remove({})
        #db.authors.remove({})
        '''
        for tw in JSONTweetsList:
            print(tw)
            if db.tweets.find_one({"_id": tw['tweet_id']}) is None:
                db_tweet = {"_id": tw['tweet_id']}
                del tw['tweet_id']
                # ----------------------------- encodeText(tw)
                tw['text'] = tw['text'].encode(encoding='UTF-8', errors='ignore')
                tw['keyword'] = tw['keyword'].encode(encoding='UTF-8', errors='ignore')
                tw['author']['username'] = tw['author']['username'].encode(encoding='UTF-8', errors='ignore')
                tw['author']['desc'] = tw['author']['desc'].encode(encoding='UTF-8', errors='ignore')
                # -----------------------------
                # print(len(list(db.tweets.find({"tweet_id": tw['tweet_id']}))))
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
        print(db.tweets.count(), db.authors.count())'''

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
