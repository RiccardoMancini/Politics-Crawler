import argparse
from snscrape.modules.instagram import InstagramUserScraper, InstagramHashtagScraper
from snscrape.modules.facebook import FacebookGroupScraper
from snscrape.modules.twitter import TwitterHashtagScraper
from Service.Twitter.twitter_scrape import TwitterScrape
from pymongo import MongoClient

if __name__ == '__main__':
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["twitter_scrape"]

    # Per verificare il post: https://twitter.com/i/web/status/:id_post
    twitterScrape = TwitterScrape(keyword='giorgiameloni', max_results=50).keyword_scrape(mydb)


    '''for x in mydb.authors.find({"_id": 1531728559584206848}):
        print(x)'''




