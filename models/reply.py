import time
from .mongo import Mongo


class Reply(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('content', str, ''),
        ('topic_id', int, -1),
        ('receiver_id', int, -1),
        ('user_id', int, -1)
    ]

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.save()


# def save(data, path):
#     """
#     data是dict或者list
#     path是保存文件的路径
#     """
#     s = json.dumps(data, indent=2, ensure_ascii=False)
#     with open(path, 'w+', encoding='utf-8') as f:
#         f.write(s)


# class Reply(Model):
#     def __init__(self, form):
#         self.id = None
#         self.content = form.get('content', '')
#         self.ct = int(time.time())
#         self.ut = self.ct
#         self.topic_id = int(form.get('topic_id', -1))
#
#     def user(self):
#         from .user import User
#         u = User.find(self.user_id)
#         return u
#
