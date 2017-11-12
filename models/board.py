import time
from models import Model
from models.mongo import Charley

# class Board(Model):
#     def __init__(self, form):
#         self.id = None
#         self.board_name = form.get('board_name', '')
#         self.ct = int(time.time())
#         self.ut = self.ct


class Board(Charley):
    __fields__ = Charley.__fields__ + [
        ('title', str, '')
    ]
