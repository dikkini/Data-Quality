#-*- coding: utf8 -*-

import sqlite3
import wx
import logging
logging.basicConfig(filename='file.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

# Класс для работы с локальной базой данных. Загрузка, добавление, удаление регулярных выражений
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
            name = u'%s_%s' % (self.schema, self.table)
            #name = name.encode('utf8')
            #regexp = regexp.encode('utf8')
            #data = (unicode(name), unicode(regexp))
            data = (name, regexp)
            self.db.execute(u'create table if not exists %s (name, regexp)' % param)
            self.db.execute(u'insert into %s values(?, ?)' % param, data)
            self.db.commit()
            logging.info(u'uploading regular expression %s for parameter %s successfully' % (regexp, param))
        except (sqlite3.DatabaseError, sqlite3.DataError, sqlite3.OperationalError), info:
            wx.MessageBox(str(info))
            info = str(info)
            info = info.encode('utf8')
            logging.error(u'failed to upload regular expression %s for parameter %s: %s' % (regexp, param))

    def del_regexp(self, param, regexp):
        try:
            name = u'%s_%s' % (self.schema, self.table)
            what_delete = (name, regexp)
            self.db.execute(u'DELETE FROM %s WHERE name=? and regexp=?' % param, what_delete)
            self.db.commit()
            logging.info(u'deleting regular expression %s for parameter %s successfully' % (regexp, param))
        except (sqlite3.DatabaseError, sqlite3.DataError, sqlite3.OperationalError), info:
            wx.MessageBox(str(info))
            logging.error(u'deleting regular expression %s for parameter %s failed: %s' % (regexp, param))

    def take_regexps(self, param):
        try:
            rows = []
            data = []
            name = u'%s_%s' % (self.schema, self.table)
            self.db.execute(u'create table if not exists %s (name, regexp)' % param)
            cur = self.db.execute(u'SELECT regexp FROM %s WHERE name="%s"' % (param, name))
#            for row in cur:
#                rows.append(map(lambda a: a.encode(u'utf-8'), row))
            for row in cur:
                data.append(row[0])
            logging.info(u'loading regular expressions for parameter %s successfully ' % (param))
        except (sqlite3.DatabaseError, sqlite3.DataError, sqlite3.OperationalError), info:
            wx.MessageBox(str(info))
            logging.error(u'loading regular expressions for parameter %s failed: %s' % (param))
        finally:
            return data