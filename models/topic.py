from pymongo import MongoClient
from .mongo import Mongo
from .user import User
from .reply import Reply
from .board import Board
from utils import log


class Topic(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('views', int, 0),
        ('title', str, ''),
        ('content', str, ''),
        ('user_id', int, -1),
        ('board_id', int, -1),
        ('top', bool, False),
    ]

    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def replies(self):
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def board_name(self):
        m = Board.find(self.board_id)
        return m.board_name

    def user_name(self):
        m = User.find(self.user_id)
        return m.username

    def user(self):
        m = User.find_by(id=self.user_id)
        return m

    def board_name(self, board_id=0):
        board = Board.find(board_id)
        return board.board_name

    @classmethod
    def find_page(cls, query_filter=None, page_size=15, page_no=1, **kwargs):
        client = MongoClient("localhost", 27017)
        collection = client.db['Topic']
        skip = page_size * (page_no - 1)
        ds = collection.find(query_filter).sort([('created_time', -1)]).limit(page_size).skip(skip)
        l = [cls._new_with_bson(d) for d in ds]
        return l

