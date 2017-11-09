import time
from models import Model


def save(data, path):
    """
    data是dict或者list
    path是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


class Reply(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.ct = int(time.time())
        self.ut = self.ct
        self.topic_id = int(form.get('topic_id', -1))

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u

    @classmethod
    def delete(cls, topic_id):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == topic_id:
                index = i
                break
        if index == -1:
            # 没找到
            pass
        else:
            obj = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save[l, path]
            return obj
