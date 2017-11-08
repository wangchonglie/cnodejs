import json
from utils import log


def save(data, path):
    """
    data是dict或者list
    path是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


class Model(object):
    """
    Model 是所有model的基类
    """
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def _new_from_dict(cls, d):
        # 因为子元素的__init__需要一个form的参数
        # 所以这个给一个空字典
        m = cls({})
        # log('m是什么，类型是？', m, type(m))
        for k, v in d.items():
            # setattr是一个特殊的函数
            # 假设k, v分别是'name' 'gua'
            # 它相当于 m.name = 'gua'
            setattr(m, k, v)
        return m

    @classmethod
    def new(cls, form, **kwargs):
        m = cls(form)
        # 格外地设置m的属性
        for k, v in kwargs.items():
            # setattr，可以设置对象的属性
            setattr(m, k, v)
        m.save()
        return m

    @classmethod
    def all(cls):
        """
        all 方法（类里面的函数叫方法）使用load 函数得到所有的models
        """
        path = cls.db_path()
        models = load(path)
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # 因为这里是从 存储的数据文件 中加载所有的数据
        # 所以用 _new_from_dict 这个特殊的函数来初始化一个数据
        ms = [cls._new_from_dict(m) for m in models]
        return ms

    @classmethod
    def find_all(cls, **kwargs):
        ms = []
        k, v = '', ''
        for key, value in kwargs.items():
            k,v = key, value
        all = cls.all()
        for m in all:
            # 也可以用getattr(m, k)取值
            if v == m.__dict__[k]:
                ms.append(m)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        kwargs 是只有一个元素的dict
        """
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def get(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        for i, e in enumerate(models):
            if e.id == id:
                index = i
                break
        if index == -1:
            # 没找到
            pass
        else:
            obj = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)
            # 返回被删除的元素
            return obj

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说， 它的作用是得到类的字符串表达形式
        比如print(u)实际上是print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: {}'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def json(self):
        """
        返回当前model 的字典表示
        """
        # copy 会复制一份新数据并返回
        d = self.__dict__.copy()
        return d

    def save(self):
        """
        用all 方法读取文件中的所有model 并生成一个list
        把self 添加进去并且保存进文件
        """
        models = self.all()
        # 如果没有id，说明是新添加的元素
        if self.id is None:
            # 设置self.id
            # 先看看是否是空list
            if len(models) == 0:
                # 我们让第一个元素的id为1（也可以为0）
                self.id = 1
            else:
                m = models[-1]
                self.id = m.id + 1
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            models[index] = self
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)



















