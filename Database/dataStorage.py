__author__ = 'aydar'

import MySQLdb
import config
import UserData


class Database:
    def __init__(self):
        self.storage = {}
        self.db = MySQLdb.connect(host=config.db_host, user=config.db_username, passwd=config.db_password, db="telegraggdb", charset='utf8')
        self.db.autocommit(True)

    def get_user(self, user_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT id, name, creation_time FROM users WHERE id=%s', [user_id])

        rows = cursor.fetchall()

        if rows and len(rows)>0:
            user = UserData.User()
            user.id, user.name, user.creation_time = rows[0]
            return user
        else:
            return None

    def create_user(self, user):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO users(id,name) values(%s,%s)', (user.id, user.name))
        self.db.commit()

    def add_email(self, user_id, email_settings):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO user_emails(user_id, type, email,auth_data) values(%s,%s, %s, %s)',
                       (user_id, email_settings.type, email_settings.email, email_settings.auth_data))
        self.db.commit()

    def get_emails(self, user_id):
        cursor = self.db.cursor()

        cursor.execute('SELECT email, type, auth_data from user_emails WHERE user_id=%s', [user_id])

        rows = cursor.fetchall()

        result = []
        if rows and len(rows) > 0:
            for row in rows:
                email = UserData.EmailSettings()
                email.email, email.type, email.auth_data = row
                result.append(email)

        return result

    def get_all_users(self):
        cursor = self.db.cursor()

        cursor.execute('SELECT id from users')

        rows = cursor.fetchall()

        result = []
        if rows and len(rows) > 0:
            for row in rows:
                user = UserData.User()
                user.id = row[0]
                user.emails = self.get_emails(user.id)

                result.append(user)
        return result