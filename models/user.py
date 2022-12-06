class User(object):
    def __init__(self, id, username, email, provider, confirmed, blocked, createdAt, updatedAt):
        self.id = id
        self.username = username
        self.email = email
        self.provider = provider
        self.confirmed = confirmed
        self.blocked = blocked
        self.createdAt = createdAt
        self.updatedAt = updatedAt