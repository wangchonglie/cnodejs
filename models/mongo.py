import time
from pymongo import MongoClient
from utils import log

Charley = MongoClient()


def timestamp():
    return int(time.time())


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    # 存储数据的id
    doc = Charley.db['data_id']
    # find_and_modify 是一个原子操作函数
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


class Mongo(object):
    __fields__ = [
        '_id',
        # （字段名， 类型， 值）
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('created_time', int, 0),
        ('updated_time', int, 0),
    ]

    @classmethod
    def has(cls, **kwargs):
        """
        检查一个元素是否在数据库中，用法如下：User.has(id=1)
        """
        return cls.find_one(**kwargs) is not None

    def mongos(self, name):
        return Charley.db[name]._find()

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    @classmethod
    def new(cls, form=None, **kwargs):
        # new 是给外部使用的函数
        name = cls.__name__
        # 创建一个空对象
        m = cls()
        # 把定义的数据写入空对象， 未定义的数据输出错误
        fields = cls.__fields__.copy()
        # 去掉_id 这个特殊的字段
        fields.remove('_id')
        if form is None:
            form = {}
        for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                # 设置默认值
                setattr(m, k, v)
        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        # 写入默认数据
        m.id = next_id(name)
        ts = int(time.time())
        m.created_time = ts
        m.updated_time = ts
        m.type = name.lower()
        # 特殊model 的自定义设置
        # m._setup(form)
        m.save()
        return m

    @classmethod
    def _new_with_bson(cls, bson):
        """
        这是给内部all 这种函数使用的函数
        从mongo数据中恢复一个model
        """
        m = cls()
        fields = cls.__fields__.copy()
        # 去掉 _id 这个特殊的字段
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                # 设置默认值
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        """
        这一句必不可少，否则bson生成一个新的_id
        FIXME,因为现在的数据库里面未必有tyoe
        所以在这里强行加上
        以后洗掉db的数据后应该删掉这一句
        """
        m.type = cls.__name__.lower()
        return m

    @classmethod
    def all(cls):
        # 按照id升序排序
        # name = cls.__name
        # ds = Charley.db[name].find()
        # l = [cls._new_with_bson(d) for d in ds]
        # return l
        return cls._find()

    @classmethod
    def _find(cls, **kwargs):
        # mongo数据查询
        name = cls.__name__
        # TODO 过滤掉被删除的元素
        kwargs['deleted'] = False
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = Charley.db[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]

        return l

    @classmethod
    def _find_raw(cls, **kwargs):
        name = cls.__name__
        ds = Charley.db[name]._find(kwargs)
        l = [d for d in ds]
        return l

    @classmethod
    def _clean_field(cls, source, target):
        """
        清洗数据用的函数
        例如 User._clean_field('is_hidden', 'deleted')
        把is_hidden字段全部复制为deleted字段
        """
        ms = cls._find()
        for m in ms:
            v = getattr(m, source)
            setattr(m, target, v)
            m.save()

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def find(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def get(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def find_one(cls, **kwargs):
        """
        """
        # TODO 过滤掉被删除的元素
        kwargs['deleted'] = False
        l = cls._find(**kwargs)
        # print('find one debug', kwargs, l)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def find_except(cls, **kwargs):
        # TODO 过滤掉被删除的元素
        kwargs['deleted'] = False
        l = cls._find(**kwargs)
        # print('find one debug', kwargs, l)
        if len(l) > 0:
            return l
        else:
            return None

    @classmethod
    def upsert(cls, query_form, update_form, hard=False):
        ms = cls.find_one(**query_form)
        if ms is None:
            query_form.update(**update_form)
            ms = cls.new(query_form)
        else:
            ms.update(update_form, hard=hard)
        return ms

    def update(self, form, hard=False):
        for k, v in form.items():
            if hard or hasattr(self, k):
                setattr(self, k, v)
        # self.updated_time = int(time.time()) fixme
        self.save()

    def save(self):
        name = self.__class__.__name__
        Charley.db[name].save(self.__dict__)

    def delete(self):
        name = self.__class__.__name__
        query = {
            'id': self.id,
        }
        values = {
            'deleted': True
        }
        # Charley.db[name].update_one(query, values)
        self.deleted = True
        self.save()

    def blacklist(self):
        b = [
            '_id',
        ]
        return b

    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        # TODO, 增加一个 type 属性
        return d

    def data_count(self, cls):
        """
        神奇的函数, 查看用户发表的评论数
        u.data_count(Comment)

        :return: int
        """
        name = cls.__name__
        # TODO, 这里应该用 type 替代
        fk = '{}_id'.format(self.__class__.__name__.lower())
        query = {
            fk: self.id,
        }
        count = Charley.db[name]._find(query).count()
        return count

    # 查看发布时间
    @classmethod
    def new_time(cls, ct):
        time_now = int(time.time())
        distance_time = time_now - ct
        h = distance_time / 3600
        log(h)
        if h < 1:
            minutes = int(distance_time / 60)
            return str(minutes) + '分钟'
        elif h < 24:
            hours = int(h)
            return str(hours) + '小时'
        else:
            days = int(h / 24)
            return str(days) + '天'
