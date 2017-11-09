import time
from models import Model


class Board(Model):
    def __init__(self, form):
        self.id = None
        self.board_name = form.get('board_name', '')
        self.ct = int(time.time())
        self.ut = self.ct
