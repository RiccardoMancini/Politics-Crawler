import json


class Author:
    """
    This class represent the author of the tweet on Twitter
    """

    def __init__(self, user_id: str, username: str, description: str, follower: int, following: int,
                 n_statuses: int, n_favourites: int, n_media: int):

        self.user_id = user_id
        self.username = username
        self.desc = description
        self.follower = follower
        self.following = following
        self.n_statuses = n_statuses
        self.n_favourites = n_favourites
        self.n_media = n_media


class AuthorEncoder(json.JSONEncoder):
    def default(self, o: Author) -> dict:
        dictionary = {}
        for k in o.__dict__:
            dictionary[k] = o.__dict__[k]
        return dictionary
