from models import Mongo


class Board(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('tab', str, ''),
        ('board_name', str, ''),
        ('deleted', bool, False),
    ]

