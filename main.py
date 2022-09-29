import argparse
from snscrape.modules.instagram import InstagramUserScraper, InstagramHashtagScraper
from snscrape.modules.facebook import FacebookGroupScraper
from snscrape.modules.twitter import TwitterHashtagScraper
from Service.Twitter.twitter_scrape import TwitterScrape
from pymongo import MongoClient
from datetime import date

if __name__ == '__main__':
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["twitter_scrape"]
    # mydb.tweets.remove({})
    # mydb.authors.remove({})

    # Per verificare il post: https://twitter.com/i/web/status/:id_post
    TwitterScrape(keyword='matteorenzi',
                  max_results=50,
                  since=date(2022, 9, 23),
                  until=date(2022, 9, 25)).keyword_scrape(mydb)

    for x in mydb.tweets.aggregate([{"$group": {"_id": '$keyword', "count": {"$count": {}}}}]):
        print(x)

    '''for x in mydb.tweets.aggregate([{"$group": {"_id": '$author', "count": {"$sum": 1}}}]):
        print(x)'''

    '''for x in mydb.tweets.find({}):
        print(x)'''




