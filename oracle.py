# -*- coding: utf-8 -*-
import cx_Oracle
from itertools import chain
import wx
import logging
logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class WorkDB():
    def __init__(self, connection):
        self.connection = connection

    def get_tables(self, schema):
        try:
            cursor = cx_Oracle.Cursor(self.connection)
            # Получать все таблицы доступные пользователю.
            sql = ("select TABLE_NAME from dba_tables WHERE OWNER = '%s'" % schema)
            cursor.execute(sql)
            tables = cursor.fetchall()
            tables=[i[0] for i in tables]
            cursor.close()
            return tables
        except Exception, info:
            info = str(info)
            info = info.decode('cp1251').encode('utf8')
            wx.MessageBox(u'Внешняя ошибка базы данных:%s - code 25' % info)
            logging.error(u'loading list of tables failed - code 26:', str(info))

    def get_schemas(self):
        try:
            cursor = cx_Oracle.Cursor(self.connection)
            sql = ("select USERNAME from dba_users")
            cursor.execute(sql)
            schemas = cursor.fetchall()
            schemas=[i[0] for i in schemas]
            cursor.close()
            return schemas
        except TypeError, info:
            wx.MessageBox(u'Подключитесь к базе данных!')

    def get_all_count(self, schema, table):
        try:
            cursor = cx_Oracle.Cursor(self.connection)
            sql = ("select count(*) from %s.%s") % (schema, table)
            cursor.execute(sql)
            data=cursor.fetchall()
            count = data[0][0]
            cursor.close()
            return count
        except (cx_Oracle.DatabaseError, cx_Oracle.DataError), info:
            info = str(info)
            info = info.decode('cp1251').encode('utf8')
            wx.MessageBox(u'Внешняя ошибка базы данных: %s - code 52' % info)
            
    def get_regexp_count(self, schema, table, regexp):
        try:
            cursor = cx_Oracle.Cursor(self.connection)
            sql = (u"select count(*) from %s.%s where %s") % (schema, table, regexp)
            cursor.execute(sql)
            data=cursor.fetchall()
            count = data[0][0]
            cursor.close()
            return count
        except (cx_Oracle.DatabaseError, cx_Oracle.DataError), info:
            info = str(info)
            info = info.decode('cp1251').encode('utf8')
            wx.MessageBox(u'Внешняя ошибка базы данных: %s - code 66' % info)

    def get_empty_values(self, schema, table):
        try:
            cursor = cx_Oracle.Cursor(self.connection)
            sql = ("select * from %s.%s" % (schema, table))
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
            data = list(chain(*data))
            all_data = len(data)
            DWEV = filter(bool, data)
            EV = all_data - len(DWEV)
            EV = float(EV)
            return EV
        except (cx_Oracle.DatabaseError, cx_Oracle.DataError), info:
            info = str(info)
            info = info.decode('cp1251').encode('utf8')
            wx.MessageBox(u'Внешняя ошибка базы данных: %s - code 84' % info)

    def get_uniq_values(self, column, schema, table):
        try:
            cursor = cx_Oracle.Cursor(self.connection)
            sql = "select DISTINCT(count(%s)) from %s.%s" % (column, schema, table)
            cursor.execute(sql)
            count = cursor.fetchall()
            cou = count[0][0]
            cursor.close()
            return cou
        except (cx_Oracle.DatabaseError, cx_Oracle.DataError), info:
            info = str(info)
            info = info.decode('cp1251').encode('utf8')
            wx.MessageBox(u'Внешняя ошибка базы данных - code 98')

    def get_cols(self, table):
        try:
            cursor = cx_Oracle.Cursor(self.connection)
            sql = ("select t.COLUMN_ID, t.COLUMN_NAME from all_tab_columns t where t.TABLE_NAME=\'%s\' order by t.COLUMN_ID") % table
            cursor.execute(sql)
            cuu=cursor.fetchall()
            cursor.close()
            col_names = [i[1] for i in cuu]
        except (NameError, cx_Oracle.DatabaseError), info:
            info = str(info)
            info = info.decode('cp1251').encode('utf8')
            error = ("Database Error: %s - code 111" % info)
            wx.MessageBox(str(error))
        return col_names

    def get_date_table(self, table, schema):
        try:
            cursor = cx_Oracle.Cursor(self.connection)
            sql = ("select created from dba_objects where owner=\'%s\' and object_name=\'%s\' and object_type=\'TABLE\'" % (schema, table))
            cursor.execute(sql)
            count = cursor.fetchall()
            date = count[0][0]
            cursor.close()
        except (cx_Oracle.DatabaseError, cx_Oracle.DataError), info:
            info = str(info)
            info = info.decode('cp1251').encode('utf8')
            wx.MessageBox(u'Внешняя ошибка базы данных - code 126')
        return date
            