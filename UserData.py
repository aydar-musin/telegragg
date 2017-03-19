__author__ = 'aydar'


class User:
    def __init__(self):
        self.id = None
        self.emails = []


class EmailSettings:
    def __init__(self):
        self.email = None
        self.password = None
        self.imap_host = None
        self.imap_port = None