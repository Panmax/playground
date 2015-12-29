from leancloud import Object as LObject


class User(LObject):
    @property
    def username(self):
        return self.get('username')

    @property
    def email(self):
        return self.get('email')
