import argparse
from snscrape.modules.instagram import InstagramUserScraper, InstagramHashtagScraper
from snscrape.modules.facebook import FacebookGroupScraper
from snscrape.modules.twitter import TwitterHashtagScraper
from Service.Twitter.twitter_scrape import TwitterScrape
from pymongo import MongoClient
from datetime import date

# Per verificare il post: https://twitter.com/i/web/status/:id_post

if __name__ == '__main__':
    # Parameters for scraping
    keywords = ['meloni']
    date_i = date(2022, 9, 19)
    date_f = date(2022, 9, 24)
    max_tweets = 50

    # MongoDB connection
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["twitter_scrape"]
    # mydb.tweets.delete_many({})
    # mydb.authors.delete_many({})

    # Extraction of tweets by @keywords
    '''for keyword in keywords:
        print('Scraping tweets with keyword: ', keyword)
        TwitterScrape(keyword=keyword,
                      since=date_i,
                      until=date_f).keyword_scrape(mydb)'''

    print(mydb.tweets.count_documents({}), mydb.authors.count_documents({}))

    # Some queries...
    '''for x in mydb.tweets.find({"keyword": [b'giorgiameloni']})[:100]:
        print(x['text'], x['media_url'], x['keyword'])'''

    for x in mydb.tweets.aggregate([
        {"$unwind": "$keyword"},
        {"$group": {"_id": '$keyword', "count": {"$count": {}}}}]):
        print(x)

    for x in mydb.tweets.find({})[150000:150100]:
        print(x['text'], x['media_url'], x['keyword'])
