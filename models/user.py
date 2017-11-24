from .mongo import Mongo



class User(Mongo):
    __fields__ = Mongo.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('role', int, 11),
        ('user_image', str, 'default.png'),
        ('signature', str, '这家伙很懒，什么个性签名都没有留下。'),
    ]

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
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User()
        u.username = form.get('username', '')
        u.password = form.get('password', '')
        user = User.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None




