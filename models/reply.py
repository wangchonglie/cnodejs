import time
from .mongo import Mongo
from .user import User


class Reply(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('content', str, ''),
        ('topic_id', int, -1),
        ('receiver_id', int, -1),
        ('user_id', int, -1)
    ]

    def user(self):
        u = User.find(self.user_id)
        return u

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.save()

