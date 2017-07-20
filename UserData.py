__author__ = 'aydar'


class User:
    def __init__(self):
        self.id = None
        self.name = None
        self.creation_time = None
        self.emails = []


class EmailSettings:
    def __init__(self):
        self.email = None
        self.type = None
        self.auth_data = None
