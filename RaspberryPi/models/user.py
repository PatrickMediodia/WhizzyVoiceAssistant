class User(object):
    def __init__(self, id, username, email, provider, confirmed, blocked, createdAt, updatedAt, account_type, full_name, uid, passcode):
        self.id = id
        self.username = username
        self.email = email
        self.provider = provider
        self.confirmed = confirmed
        self.blocked = blocked
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.account_type = account_type
        self.full_name = full_name
        self.uid = uid
        self.passcode = passcode