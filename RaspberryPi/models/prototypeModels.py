class Room:
    def __init__(self, id, attributes):
        self.id = id
        self.attributes = RoomAttributes(**attributes)

class RoomAttributes:
    def __init__(self, createdAt, updatedAt, publishedAt, name, devices):
        self.createdAt = createdAt,
        self.updatedAt = updatedAt,
        self.publishedAt = publishedAt,
        self.name = name
        self.devices = [ Device(**device) for device in devices['data'] ]
    
class Device:
    def __init__(self, id, attributes):
        self.id = id
        self.attributes = DeviceAttributes(**attributes)

class DeviceAttributes:
    def __init__(self, name, identifier, status, createdAt, updatedAt, publishedAt):
        self.name = name
        self.identifier = identifier
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.publishedAt = publishedAt
