import time
from models import Model
from models.mongo import Mongo

# class Board(Model):
#     def __init__(self, form):
#         self.id = None
#         self.board_name = form.get('board_name', '')
#         self.ct = int(time.time())
#         self.ut = self.ct


class Board(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('board_name', str, ''),
        ('deleted', bool, False),
    ]

