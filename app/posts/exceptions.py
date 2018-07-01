class DuplicateRelationExceptionPost(Exception):
    def __init__(self, post, user, likes_type):
        self.post = post
        self.user = user
        self.likes_type = likes_type


class FollowRelationNotExistPost(Exception):
    def __init__(self, post, user, likes_type):
        self.post = post
        self.user = user
        self.likes_type = likes_type
