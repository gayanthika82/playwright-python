class TokenStore:
    token = None

    @classmethod
    def set_token(cls, token):
        cls.token = token

    @classmethod
    def get_token(cls):
        return cls.token
