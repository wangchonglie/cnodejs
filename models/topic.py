import time
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
        m = User.find(self.user_id)
        return m


# class Topic(Model):
#     def __init__(self, form):
#         self.id = None
#         self.views = 0
#         self.title = form.get('title', '')
#         self.content = form.get('content', '')
#         self.ct = int(time.time())
#         self.ut = self.ct
#         self.user_id = form.get('user_id', '')
#         self.board_id = int(form.get('board_id', -1))
#
#     @classmethod
#     def get(cls, id):
#         m = cls.find_by(id=id)
#         m.views += 1
#         m.save()
#         return m
#
#     def replies(self):
#         from .reply import Reply
#         ms = Reply.find_all(topic_id=self.id)
#         return ms
#
#     def board_name(self):
#         from .board import Board
#         m = Board.find(self.board_id)
#         # log('board', m)
#         return m.board_name
#
#     def user_name(self):
#         from .user import User
#         m = User.find(self.user_id)
#         log('user', m)
#         return m.username
#
#     def user(self):
#         from models.user import User
#         m = User.find(self.id)
#         return m


