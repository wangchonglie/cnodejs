import time
from pymongo import MongoClient
from .mongo import Mongo
from utils import log


class Topic(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('views', int, 0),
        ('title', str, ''),
        ('content', str, ''),
        ('user_id', int, -1),
        ('board_id', int, -1),
    ]

    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def board_name(self):
        from .board import Board
        m = Board.find(self.board_id)
        # log('board', m)
        return m.board_name

    def user_name(self):
        from .user import User
        m = User.find(self.user_id)
        return m.username

    def user(self):
        from models.user import User
        m = User.find_by(id=self.user_id)
        return m

    @classmethod
    def find_page(cls, query_filter=None, page_size=15, page_no=1, **kwargs):
        client = MongoClient("localhost", 27017)
        collection = client.db['Topic']
        kwargs['deleted'] = False
        flag_sort = '__sort'
        skip = page_size * (page_no - 1)
        sort = kwargs.pop(flag_sort, None)
        ds = collection.find(query_filter).limit(page_size).skip(skip)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        return l


