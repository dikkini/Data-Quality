#-*- coding: utf8 -*-

import sqlite3
import wx
import logging
logging.basicConfig(filename='file.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class sqliteDB():
    def __init__(self, schema, table):
        try:
            self.schema = schema
            self.table = table
            self.db = sqlite3.connect('./data_quality.db')
            logging.info(u'connecting to local database successfully')
        except (sqlite3.DatabaseError, sqlite3.DataError, sqlite3.OperationalError), info:
            wx.MessageBox(str(info))
            logging.info(u'connecting to local database failed', str(info))
            
            
# methods to working with regexps: add, del, take all.

    def add_regexp(self, param, regexp):
        try:
            name = '%s_%s' % (self.schema, self.table)
            data = (unicode(name), unicode(regexp))
            self.db.execute('create table if not exists %s (name, regexp)' % param)
            self.db.execute('insert into %s values(?, ?)' % param, data)
            self.db.commit()
            logging.info(u'uploading regular expression %s for parameter %s successfully' % (regexp, param))
        except (sqlite3.DatabaseError, sqlite3.DataError, sqlite3.OperationalError), info:
            wx.MessageBox(str(info))
            print info
            logging.error(u'failed to upload regular expression %s for parameter %s: %s' % (regexp, param, str(info)))

    def del_regexp(self, param, regexp):
        try:
            name = '%s_%s' % (self.schema, self.table)
            what_delete = (name, regexp)
            self.db.execute('DELETE FROM %s WHERE name=? and regexp=?' % param, what_delete)
            self.db.commit()
            logging.info(u'deleting regular expression %s for parameter %s successfully' % (regexp, param))
        except (sqlite3.DatabaseError, sqlite3.DataError, sqlite3.OperationalError), info:
            wx.MessageBox(str(info))
            logging.error(u'deleting regular expression %s for parameter %s failed: %s' % (regexp, param, str(info)))

    def take_regexps(self, param):
        try:
            rows = []
            data = []
            name = '%s_%s' % (self.schema, self.table)
            self.db.execute('create table if not exists %s (name, regexp)' % param)
            cur = self.db.execute('SELECT regexp FROM %s WHERE name="%s"' % (param, name))
            for row in cur:
                rows.append(map(lambda a: a.encode('utf-8'), row))
            for s in rows:
                data.append(s[0])
            logging.info(u'loading regular expressions for parameter %s successfully ' % (param))
        except (sqlite3.DatabaseError, sqlite3.DataError, sqlite3.OperationalError), info:
            wx.MessageBox(str(info))
            logging.error(u'loading regular expressions for parameter %s failed: %s' % (param, str(info)))
        finally:
            return data

#===============================================================================
# # methods which working with connection module.
# 
#    def take_data_con(self, namecon):
#        try:
#            data = []
#            rows = []
#            sql = 'SELECT data FROM connections WHERE name = "%s"' % namecon
#            cur = self.db.execute('%s' % sql)
#            for row in cur:
#                rows.append(map(lambda a: a.encode('utf-8'), row))
#            for s in rows:
#                data.append(s[0])
#            if not data:
#                return wx.EmptyString
#            else:
#                data = data[0]
#                data = map(lambda data: data.strip("u' "), data.strip('[]').split(','))
#            return data
#            logging.info(u'loading connection %s data successfully')
#        except Exception, info:
#            logging.error(u'loading connection %s failed: %s' % (namecon, info))
# 
# 
#    def take_cons(self):
#        try:
#            data = []
#            rows = []
#            crtable = 'connections(name varchar(255), data varchar(255))'
#            self.db.execute('create table if not exists %s' % crtable)
#            self.db.commit()
#            sql = 'SELECT name FROM connections'
#            cur = self.db.execute('%s' % sql)
#            for row in cur:
#                rows.append(row)
#            for s in rows:
#                data.append(s[0])
#            return data
#            logging.info(u'connection list loaded successfully')
#        except Exception, info:
#            logging.error(u'connection list loading failed:', info)
# 
#    def add_con(self, namecon, data):
#        try:
#            sql_con = 'INSERT INTO connections (name, data) values ("%s", "%s")' % (namecon, data)
#            self.db.execute('%s' % sql_con)
#            self.db.commit()
#            logging.info(u'creating new connection %s successfully')
#        except Exception, info:
#            logging.error(u'creating new connection %s failed' % (namecon))
# 
#    def edit_con(self, namecon, data):
#        try:
#            # Короче тут пиздец полный. надо перейти на shelve.
#            sql = ('DELETE FROM connections WHERE name = "%s"' % namecon)
#            self.db.execute('%s' % sql)
#            self.db.commit()
#            sql_con = 'INSERT INTO connections (name, data) values ("%s", "%s")' % (namecon, data)
#            self.db.execute('%s' % sql_con)
#            self.db.commit()
#            logging.info(u'commiting changes to connection %s successfully' % (namecon))
#        except Exception, info:
#            logging.error(u'commiting changes to connection %s (%s) failed: %s' % (namecon, data, info))
#            
#    def del_con(self, namecon):
#        try:
#            sql = ('DELETE FROM connections WHERE name = "%s"' % namecon)
#            self.db.execute('%s' % sql)
#            self.db.commit()
#            logging.info(u'deleteing connection %s successfully')
#        except Exception, info:
#            logging.error(u'deleting connection %s failed: %s' % (namecon, info))
#===============================================================================
            
# methods which working with statistics.
#
#    def add_main_stat(self, date, data):
#        try:
#            name_table = 'main_stat_%s_%s' % (self.schema, self.table)
#            self.db.execute('create table if not exists %s(date varchar(255), data varchar(255))' % name_table)
#            self.db.commit()
#            self.db.execute('INSERT INTO %s VALUES ("%s", "%s")' % (name_table, date, data))
#            self.db.commit()
#            logging.info(u'main statistic for %s loaded successfully' % (date))
#        except (sqlite3.DatabaseError, sqlite3.DataError, sqlite3.OperationalError), info:
#            wx.MessageBox(str(info))
#            logging.error(u'main statistic for parameter %s not loaded: %s' % (date, str(info)))
#
#    def add_ext_stat(self, date, param, data):
#        try:
#            name_table = 'ext_stat_%s_%s' % (self.schema, self.table)
#            self.db.execute('create table if not exists %s(date varchar(255), param varchar(255), data varchar(255))' % name_table)
#            self.db.commit()
#            self.db.execute('INSERT INTO %s VALUES ("%s", "%s", "%s")' % (name_table, date, param, data))
#            self.db.commit()
#            logging.info(u'extended statistic for parameter %s uploaded successfully' % (param))
#        except (sqlite3.DatabaseError, sqlite3.DataError, sqlite3.OperationalError), info:
#            wx.MessageBox(str(info))
#            logging.error(u'extended statistic for %s and parameter %s not uploaded: %s' % (date, param, str(info)))
#            
#    def take_main_stat(self, date):
#        try:
#            rows = []
#            data = []
#            name_table = 'main_stat_%s_%s' % (self.schema, self.table)
#            self.db.execute('create table if not exists %s(date varchar(255), data varchar(255))' % name_table)
#            self.db.commit()
#            cur = self.db.execute('SELECT data FROM %s WHERE date="%s"' % (name_table, date))
#            for row in cur:
#                rows.append(map(lambda a: a.encode('utf-8'), row))
#            for s in rows:
#                data.append(s[0])
#            data = data[0]
#            data = map(lambda data: data.strip("u' "), data.strip('[]').split(','))
#            return data
#            logging.info(u'main statistic for %s uploaded successfully' % (date))
#            
#        except (sqlite3.DatabaseError, sqlite3.DataError, sqlite3.OperationalError), info:
#            wx.MessageBox(str(info))
#            logging.error(u'main statistic for %s and parameter %s not uploaded: %s' % (date, param, str(info)))
#
#    def take_ext_stat(self, param, date):
#        try:
#            rows = []
#            data = []
#            name_table = 'ext_stat_%s_%s' % (self.schema, self.table)
#            self.db.execute('create table if not exists %s(date varchar(255), param varchar(255), data varchar(255))' % name_table)
#            self.db.commit()
#            cur = self.db.execute('SELECT data FROM %s WHERE date="%s" and param="%s"' % (name_table, date, param))
#            for row in cur:
#                rows.append(map(lambda a: a.encode('utf-8'), row))
#            for s in rows:
#                data.append(s[0])
#            data = data[0]
#            data = map(lambda data: data.strip("u' "), data.strip('[]').split(','))
#            return data
#            logging.error(u'extended statistic for %s and parameter %s loaded successfully' % (date, param, str(info)))
#            
#        except (sqlite3.DatabaseError, sqlite3.DataError, sqlite3.OperationalError), info:
#            wx.MessageBox(str(info))
#            logging.error(u'extended statistic for %s and parameter %s not loaded: %s' % (date, param, str(info)))