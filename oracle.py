# -*- coding: cp1251 -*- 
import cx_Oracle
from itertools import chain
import wx
import logging
logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class WorkDB():
    def __init__(self, connection):
        self.connection = connection

    def get_tables(self, schema):
        cursor = cx_Oracle.Cursor(self.connection)
        # �������� ��� ������� ��������� ������������.
        sql = ("select TABLE_NAME from dba_tables WHERE OWNER = '%s'" % schema)
        cursor.execute(sql)
        tables = cursor.fetchall()
        tables=[i[0] for i in tables]
        cursor.close()
        return tables

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
            wx.MessageBox(u'������������ � ���� ������!')
            print info
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
            wx.MessageBox(u'������� ������ ���� ������')
            print info
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
            wx.MessageBox(u'������� ������ ���� ������')
            print info

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
            wx.MessageBox(u'������� ������ ���� ������')
            print info

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
            wx.MessageBox(u'������� ������ ���� ������')
            print info

    def get_cols(self, table):
        try:
            cursor = cx_Oracle.Cursor(self.connection)
            sql = ("select t.COLUMN_ID, t.COLUMN_NAME from all_tab_columns t where t.TABLE_NAME=\'%s\' order by t.COLUMN_ID") % table
            cursor.execute(sql)
            cuu=cursor.fetchall()
            cursor.close()
            col_names = [i[1] for i in cuu]
        except (NameError, cx_Oracle.DatabaseError), info:
            error = ("Database Error: %s" % info)
            wx.MessageBox(str(error))
        return col_names