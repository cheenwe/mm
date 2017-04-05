# encoding=utf-8
from sqlhelper import SqlHelper

sql = SqlHelper()

def insert_data_to_users():
	command = ("INSERT IGNORE INTO users "
						"(id, name, created_at, remark)"
						"VALUES(%s, %s, %s, %s)")
	return command


command = insert_data_to_users()

msg = (None, "112", "", "",)

sql.insert_data(command, msg, commit = True)

print 'created user success'
