from typing import Union

from DataModel.Twitter.reaction import Reaction, ReactionEncoder
from DataModel.Twitter.author import Author, AuthorEncoder
import json
import ast


class Tweet:
    """
    This class defines the post data structure
    """

    def __init__(self, tweet_id: str, author: Author, text: str, media_url: Union[str, list], reaction: Reaction, keyword: str):
        """
        To init the object the information about
        :param author: the authors of the post
        :param text: the text connected to the post
        :param media_url: the url of the associated media
        :param reaction: the @Reaction datastructure
        """
        self.tweet_id = tweet_id
        self.author = author
        self.text = text
        self.media_url = media_url
        self.reaction = reaction
        self.keyword = keyword


class TweetEncoder(json.JSONEncoder):
    def default(self, o: Tweet) -> dict:
        dictionary = {}
        for k in o.__dict__:
            if k == 'author':
                dictionary[k] = ast.literal_eval(AuthorEncoder().encode(o.__dict__[k]))
            elif k == 'reaction':
                dictionary[k] = ast.literal_eval(ReactionEncoder().encode(o.__dict__[k]))
            else:
                dictionary[k] = o.__dict__[k]

        return dictionary
