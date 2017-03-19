__author__ = 'aydar'


class Database:
    def __init__(self):
        self.storage = {}

    def update_user(self, user):
        self.storage[user.id] = user

    def get_user(self, user_id):
        if user_id in self.storage:
            return self.storage[user_id]
        else:
            return None

    def get_all_users(self):
        return self.storage.values()
