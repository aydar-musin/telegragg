__author__ = 'aydar'

import MySQLdb
import config


db = MySQLdb.connect(host=config.db_host, user=config.db_username, passwd=config.db_password, db="telegraggdb", charset='utf8')

cursor = db.cursor()

cursor.execute('truncate table user_emails')
db.commit()
cursor.execute('delete from users')
db.commit()

