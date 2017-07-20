import MySQLdb
import config


db = MySQLdb.connect(host=config.db_host, user=config.db_username, passwd=config.db_password, db="telegraggdb", charset='utf8')

cursor = db.cursor()

sql = """
DROP TABLE IF EXISTS user_emails;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id int primary key,
    name varchar(100),
    creation_time TIMESTAMP default CURRENT_TIMESTAMP
);

CREATE TABLE user_emails(
    id int primary key auto_increment,
    user_id int,
    email varchar(100) NULL,
    type varchar(100) NOT NULL,
    auth_data varchar(5000),
    creation_time TIMESTAMP default CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id)
        REFERENCES users(id)
);
"""

cursor.execute(sql)

db.close()