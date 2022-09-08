import argparse
from snscrape.modules.instagram import InstagramUserScraper, InstagramHashtagScraper
from snscrape.modules.facebook import FacebookGroupScraper
from snscrape.modules.twitter import TwitterHashtagScraper
from Service.Twitter.twitter_scrape import TwitterScrape

if __name__ == '__main__':
    '''parser = argparse.ArgumentParser()
    parser.add_argument('--configuration_file', '-cf', required=True, help="Represent the path for configuration file.")
    args = parser.parse_args()'''
    '''scraper = TwitterHashtagScraper('', 5)
    print('here!')
    for x in list(scraper.get_items())[:10]:
        print(x)'''

    twitterScrape = TwitterScrape(profile='mybxstxrdsoul', max_results=10).profile_scrape()

