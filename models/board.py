import time
from models import Model
from models.mongo import Mongo


class Board(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('tab', str, ''),
        ('board_name', str, ''),
        ('deleted', bool, False),
    ]

