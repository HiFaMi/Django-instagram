class FollowRelationNotExist(Exception):
    def __init__(self, from_user, to_user, relation_type):
        self.from_user = from_user
        self.to_user = to_user
        self.relation_type = relation_type

    def __str__(self):
        return 'Relation (Form: {}, To: {}, Type: {})'.format(
            self.from_user,
            self.to_user,
            self.relation_type,
        )


class BaseRelationException(Exception):
    def __init__(self, from_user, to_user, relation_type):
        self.from_user = from_user
        self.to_user = to_user
        self.relation_type = relation_type


class RelationNotExist(Exception):
    def __init__(self, from_user, to_user, relation_type):
        self.from_user = from_user
        self.to_user = to_user
        self.relation_type = relation_type


class DuplicateRelationException(Exception):
    def __init__(self, from_user, to_user, relation_type):
        self.from_user = from_user
        self.to_user = to_user
        self.relation_type = relation_type

