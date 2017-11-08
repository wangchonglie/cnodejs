import time
from models import Model


class Topic(Model):
    def __init__(self, form):
        self.id = None
        self.views = 0
