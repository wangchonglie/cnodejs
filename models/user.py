from .mongo import Charley


class User(Charley):
    __fields__ = Charley.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('role', int, 11),
        ('user_image', str, ''),
    ]
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = 11
        self.user_image = 'default.png'

    def salted_password(self, password, salt='gsjkkfwk@!#'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User(form)
        user = User.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None


# class User(Model):
#     def __init__(self, form):
#         self.id = form.get('id', None)
#         self.username = form.get('username', '')
#         self.password = form.get('password', '')
#         self.role = 11
#         self.user_image = 'default.png'
#
#     def salted_password(self, password, salt='gsjkkfwk@!#'):
#         import hashlib
#         def sha256(ascii_str):
#             return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
#         hash1 = sha256(password)
#         hash2 = sha256(hash1 + salt)
#         return hash2
#
#     def hashed_password(self, pwd):
#         import hashlib
#         p = pwd.encode('ascii')
#         s = hashlib.sha256(p)
#         # 返回摘要字符串
#         return s.hexdigest()
#
#     @classmethod
#     def register(cls, form):
#         name = form.get('username', '')
#         pwd = form.get('password', '')
#         if len(name) > 2 and User.find_by(username=name) is None:
#             u = User.new(form)
#             u.password = u.salted_password(pwd)
#             u.save()
#             return u
#         else:
#             return None
#
#     @classmethod
#     def validate_login(cls, form):
#         u = User(form)
#         user = User.find_by(username=u.username)
#         if user is not None and user.password == u.salted_password(u.password):
#             return user
#         else:
#             return None



