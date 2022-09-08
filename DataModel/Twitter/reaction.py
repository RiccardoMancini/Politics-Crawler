import json
import ast
from DataModel.Twitter.comment import CommentEncoder


class Reaction:
    """
    This class describe the reaction data structure
    """

    def __init__(self, n_like: int, n_reply: int, n_retweet: int, n_quote: int):

        self.n_like = n_like
        self.n_reply = n_reply
        self.n_retweet = n_retweet
        self.n_quote = n_quote


class ReactionEncoder(json.JSONEncoder):
    def default(self, o: Reaction) -> dict:
        dictionary = {}
        for k in o.__dict__:
            dictionary[k] = o.__dict__[k]
        return dictionary
