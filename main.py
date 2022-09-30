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
    keywords = ['enricoletta', 'partitodemocratico', 'pdnetwork',
                'giorgiameloni', 'fratelliditalia',
                'matteosalvini', 'legasalvini',
                'berlusconi', 'forzaitalia', 'forza_italia'
                'giuseppeconte', 'mov5stelle']
    date_i = date(2022, 9, 23)
    date_f = date(2022, 9, 25)
    max_tweets = 50

    # MongoDB connection
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["twitter_scrape"]
    mydb.tweets.delete_many({})
    mydb.authors.delete_many({})

    # Extraction of tweets by keywords
    for keyword in keywords[:3]:
        print('Scraping tweets with keyword: ', keyword)
        TwitterScrape(keyword=keyword,
                      max_results=max_tweets,
                      since=date_i,
                      until=date_f).keyword_scrape(mydb)

    for x in mydb.tweets.aggregate([
        {"$unwind": "$keyword"},
        {"$group": {"_id": '$keyword', "count": {"$count": {}}}}]):
        print(x)

    print(mydb.tweets.count_documents({}), mydb.authors.count_documents({}))

    '''for x in mydb.tweets.aggregate([{"$group": {"_id": '$author', "count": {"$sum": 1}}}]):
        print(x)'''

    for x in mydb.tweets.find({}):
        print(x['text'], x['keyword'])
