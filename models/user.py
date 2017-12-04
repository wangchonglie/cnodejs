from models import Mongo



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
    def register(cls, username, signature, password):
        result = {}
        if User.find_by(username=username) is not None:
            result['msg'] = '该用户名已经被注册！'
            return result
        if len(username) >= 4 and len(password) >= 5:
            u = User.new()
            u.username = username
            u.signature = signature
            u.password = u.salted_password(password)
            u.save()
            result['msg'] = '注册成功！'
            return result
        else:
            result['msg'] = '用户名和密码应4位或以上！'
            return result

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




