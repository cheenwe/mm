# coding=utf-8

import utils
import logging
import config
import pymysql

class SqlHelper(object):
    def __init__(self):
        self.conn = pymysql.connect(**config.database_config)
        self.cursor = self.conn.cursor()

        try:
            self.conn.select_db(config.database)
        except:
            self.create_database()

            self.conn.select_db(config.database)

    def create_database(self):
        try:
            command = 'CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET \'utf8\' ' % config.database
            utils.log('create_database command:%s' % command)
            self.cursor.execute(command)
            self.conn.commit()
        except Exception, e:
            utils.log('SqlHelper create_database exception:%s' % str(e), logging.WARNING)

    def create_table(self, command):
        try:
            utils.log('create_table command:%s' % command)
            x = self.cursor.execute(command)
            self.conn.commit()
            return x
        except Exception, e:
            utils.log('create_table exception:%s' % str(e), logging.WARNING)

    def insert_data(self, command, data, commit = False):
        try:
            # utils.log('insert_data command:%s, data:%s' % (command, data))
            x = self.cursor.execute(command, data)
            if commit:
                self.conn.commit()
            return x
        except Exception, e:
            utils.log('insert_data exception msg:%s' % str(e), logging.WARNING)

    def commit(self):
        self.conn.commit()

    def execute(self, command, commit = True):
        try:
            utils.log('execute command:%s' % command)
            data = self.cursor.execute(command)
            if commit:
                self.conn.commit()
            return data
        except Exception, e:
            utils.log('execute exception msg:%s' % str(e))
            return None

    def query(self, command, commit = False):
        try:
            utils.log('execute command:%s' % command)

            self.cursor.execute(command)
            data = self.cursor.fetchall()
            if commit:
                self.conn.commit()
            return data
        except Exception, e:
            utils.log('execute exception msg:%s' % str(e))
            return None

    def query_one(self, command, commit = False):
        try:
            utils.log('execute command:%s' % command)

            self.cursor.execute(command)
            data = self.cursor.fetchone()
            if commit:
                self.conn.commit()

            return data
        except Exception, e:
            utils.log('execute exception msg:%s' % str(e))
            return None

    def insert_data_to_users(self):
        command = ("INSERT INTO users "
                  "(id, name,  remark)"
                  "VALUES(%s, %s, %s)")
        return command

    def insert_data_to_albums(self):
        command = ("INSERT INTO albums "
                  "(id, user_id, name, created_at, remark, kind, total)"
                  "VALUES(%s, %s, %s, %s, %s, %s, %s)")
        return command

    def insert_data_to_photos(self):
        command = ("INSERT INTO photos "
                  "(id, album_id, name, url, kind)"
                  "VALUES(%s, %s, %s, %s, %s)")
        return command

#创建表
sql = SqlHelper()
sql.create_table("create table IF NOT EXISTS  users(id bigint, name varchar(255), remark text )")
sql.create_table("create table IF NOT EXISTS albums(id bigint, user_id bigint, name varchar(255), created_at date, remark text, kind int, total float)  ")
sql.create_table("create table IF NOT EXISTS photos(id bigint, album_id bigint, name varchar(255), url varchar(255), kind int) ")
