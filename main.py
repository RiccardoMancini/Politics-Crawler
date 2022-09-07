import json
import argparse
from snscrape.modules.instagram import InstagramUserScraper, InstagramHashtagScraper
from snscrape.modules.facebook import FacebookGroupScraper
from snscrape.modules.twitter import TwitterHashtagScraper
import os
import subprocess
if __name__ == '__main__':
    '''parser = argparse.ArgumentParser()
    parser.add_argument('--configuration_file', '-cf', required=True, help="Represent the path for configuration file.")
    args = parser.parse_args()'''
    '''scraper = TwitterHashtagScraper('milan', 5)
    print('here!')
    for x in list(scraper.get_items())[:10]:
        print(x)'''

    output = subprocess.check_output('snscrape -n 5 --jsonl twitter-hashtag lega', shell=True)
    print(output.decode("utf-8"))
    '''posts_link = []
    for line in output.splitlines():
        posts_link.append(line.decode("utf-8"))
    print(posts_link)'''
