from models import Mongo


class Mail(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('title', str, ''),
        ('content', str, ''),
        ('read', bool, False),
        ('sender_id', int, -1),
        ('receiver_id', int, -1),
    ]

    def set_sender(self, sender_id):
        self.sender_id = sender_id
        self.save()

    def mark_read(self):
        self.read = True
        self.save()