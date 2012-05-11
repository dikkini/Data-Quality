
# -*- coding: utf8 -*-

import wx 
import wx.grid
import sqlite
import cx_Oracle
import fs_grid
import string
import logging
try:
    from agw import pybusyinfo as PBI
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.pybusyinfo as PBI

logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

###########################################################################
## Class RegExpEditor
###########################################################################

class page_editor():
    def __init__(self, parent, schema, table, connection):
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        self.main = parent
        self.panel_regexps = wx.Panel( self.main, wx.ID_ANY, wx.DefaultPosition, (-1,-1), wx.TAB_TRAVERSAL )
        #bSizer3.Add(self.panel_regexps, wx.EXPAND, 1)
        title_page = (u"Редактор регулярных выражений %s:%s" % (self.main.schema, self.main.table))
        self.main.notebook.AddPage( self.panel_regexps, title_page, False, wx.NullBitmap )
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.label1 = wx.StaticText( self.panel_regexps, wx.ID_ANY, u"Параметры оценки качества данных:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label1.Wrap( -1 )
        bSizer1.Add( self.label1, 0, wx.ALL, 5 )
        
        self.params_regexps_choices = [u'Не несущие информацию значения', u'Не соответствующие формату значения', 
                                       u'Значение уровня шума', u'Идентифицируемость', u'Согласованность', u'Оперативность', 
                                       u'Противоречивость', u'Достоверность', u'Степень классификации', u'Степень структуризации']
        

        self.regexp_choice_pull = wx.Choice( self.panel_regexps, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 
                                             self.params_regexps_choices, 0 )
        self.regexp_choice_pull.SetSelection( 0 )
        bSizer1.Add( self.regexp_choice_pull, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.label2 = wx.StaticText( self.panel_regexps, wx.ID_ANY, u"Регулярные выражения:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label2.Wrap( -1 )
        bSizer1.Add( self.label2, 0, wx.ALL, 5 )
        
        regexps_listboxChoices = []
        self.regexps_listbox = wx.ListBox( self.panel_regexps, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, regexps_listboxChoices, wx.LB_HSCROLL )
        bSizer1.Add( self.regexps_listbox, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.staticline = wx.StaticLine( self.panel_regexps, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer1.Add( self.staticline, 0, wx.EXPAND |wx.ALL, 5 )
        
        self.label3 = wx.StaticText( self.panel_regexps, wx.ID_ANY, u"Поле для редактирования регулярного выражения:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label3.Wrap( -1 )
        bSizer1.Add( self.label3, 0, wx.ALL, 5 )
        
        # wx.TE_MULTILINE ставит ограничение на горячую клавишу Ctrl+A.
        self.edit_regexp_txt = wx.TextCtrl( self.panel_regexps, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,150 ), wx.HSCROLL|wx.TE_MULTILINE )
        bSizer1.Add( self.edit_regexp_txt, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.add_regexp_btn = wx.Button( self.panel_regexps, wx.ID_ANY, u"Добавить регулярное выражение", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.add_regexp_btn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.del_regexp_btn = wx.Button( self.panel_regexps, wx.ID_ANY, u"Удалить регулярное выражение", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.del_regexp_btn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.checksql_btn = wx.Button( self.panel_regexps, wx.ID_ANY, u"Проверка синтаксиса SQL", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.checksql_btn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.panel_regexps.SetSizer( bSizer1 )
        self.panel_regexps.Layout()
        bSizer1.Fit( self.panel_regexps )
        bSizer3.Add( self.panel_regexps, wx.EXPAND, 1 )
        
        
#        self.main.SetSizer( bSizer3 )
#        self.Layout()
#        
#        self.Centre( wx.BOTH )
        
        #Properties
#        self.regexp_choice_pull.
        
        # Binds Events
        self.regexps_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.OnChRegexp)
        self.regexp_choice_pull.Bind(wx.EVT_CHOICE, self.OnChParamRegexp)
        self.edit_regexp_txt.Bind(wx.EVT_TEXT, self.OnEditRegexp)
                                    
        #Events Buttons
        self.checksql_btn.Bind(wx.EVT_BUTTON, self.OnTestBtn)
        self.add_regexp_btn.Bind(wx.EVT_BUTTON, self.OnAddBtn)
        self.del_regexp_btn.Bind(wx.EVT_BUTTON, self.OnDelBtn)
#        self.OK_btn.Bind(wx.EVT_BUTTON, self.OnConfirmBtn)
        
        # Variables
        self.using_params = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.weights_params = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        #SQLITE
        self.db = sqlite.sqliteDB(self.main.schema, self.main.table)
        
        #Table
        self.table = table
        self.schema = schema
        
        #Connection
        self.connection = connection
    
    def OnGridTab(self, event):
        fsg = fs_grid.fullgrid(self.grid_table)
        fsg.Show()
        self.check_grid.Destroy()               
    
    def OnChParamRegexp(self, event):
        if self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[0]:
            self.param = 'no_information'
            try:
                self.edit_regexp_txt.SetValue(self.regexp0)
            except AttributeError:
                self.edit_regexp_txt.SetValue(wx.EmptyString)
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[1]:
            self.param = 'bad_format'
            try:
                self.edit_regexp_txt.SetValue(self.regexp1)
            except AttributeError:
                self.edit_regexp_txt.SetValue(wx.EmptyString)
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[2]:
            self.param = 'noise_level'
            try:
                self.edit_regexp_txt.SetValue(self.regexp2)
            except AttributeError:
                self.edit_regexp_txt.SetValue(wx.EmptyString)
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[3]:
            self.param = 'identifiability'
            try:
                self.edit_regexp_txt.SetValue(self.regexp3)
            except AttributeError:
                self.edit_regexp_txt.SetValue(wx.EmptyString)
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[4]:
            self.param = 'harmony'
            try:
                self.edit_regexp_txt.SetValue(self.regexp4)
            except AttributeError:
                self.edit_regexp_txt.SetValue(wx.EmptyString)
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[5]:
            self.param = 'efficiency'
            try:
                self.edit_regexp_txt.SetValue(self.regexp5)
            except AttributeError:
                self.edit_regexp_txt.SetValue(wx.EmptyString)
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[6]:
            self.param = 'inconsistency'
            try:
                self.edit_regexp_txt.SetValue(self.regexp6)
            except AttributeError:
                self.edit_regexp_txt.SetValue(wx.EmptyString)
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[7]:
            self.param = 'reliability'
            try:
                self.edit_regexp_txt.SetValue(self.regexp7)
            except AttributeError:
                self.edit_regexp_txt.SetValue(wx.EmptyString)
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[8]:
            self.param = 'degree_of_classification'
            try:
                self.edit_regexp_txt.SetValue(self.regexp8)
            except AttributeError:
                self.edit_regexp_txt.SetValue(wx.EmptyString)
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[9]:
            self.param = 'degree_of_structuring'
            try:
                self.edit_regexp_txt.SetValue(self.regexp9)
            except AttributeError:
                self.edit_regexp_txt.SetValue(wx.EmptyString)
            
        items = self.db.take_regexps(self.param)
        self.regexps_listbox.SetItems(items)
            
    def OnChRegexp(self, event):
        choosed_regexp = self.regexps_listbox.GetStringSelection()
        edit_regexp = self.edit_regexp_txt.GetValue()
        if edit_regexp is None or edit_regexp == wx.EmptyString:
            self.edit_regexp_txt.SetValue(choosed_regexp)
        else:
            self.edit_regexp_txt.AppendText((u' or %s' % choosed_regexp))
    
    def OnEditRegexp(self, event):
        if self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[0]:
            self.regexp0 = self.edit_regexp_txt.GetValue()    
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[1]:
            self.regexp1 = self.edit_regexp_txt.GetValue()
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[2]:
            self.regexp2 = self.edit_regexp_txt.GetValue()
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[3]:
            self.regexp3 = self.edit_regexp_txt.GetValue()
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[4]:
            self.regexp4 = self.edit_regexp_txt.GetValue()
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[5]:
            self.regexp5 = self.edit_regexp_txt.GetValue()
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[6]:
            self.regexp6 = self.edit_regexp_txt.GetValue()
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[7]:
            self.regexp7 = self.edit_regexp_txt.GetValue()
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[8]:
            self.regexp8 = self.edit_regexp_txt.GetValue()
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[9]:
            self.regexp9 = self.edit_regexp_txt.GetValue()
    
    def OnTestBtn(self, event):
        message = 'Пожалуйста подождите, получение информации из базы...'
        try:
            busy = PBI.PyBusyInfo(message, parent=None, title="Формирование и отправка запроса к базе данных...")
            
            wx.Yield()
            
            
            cursor = cx_Oracle.Cursor(self.connection)
            regexp = self.edit_regexp_txt.GetValue()
            sql = ('select * from %s.%s where %s') % (self.schema, self.table, regexp)
            cursor.execute(sql)
            grid_data=cursor.fetchall()
            data = []
            for item in grid_data:
                data.append(map(lambda a: a.decode('cp1251') if isinstance(a, basestring) else a, item))
            if not data:
                del busy
                wx.MessageBox(u'Нет данных!')
                event.Skip()
                return
            self.grid_table = GridTable(data, self.connection, self.table)
            cursor.close()
            #self.check_grid.SetTable(self.grid_table, True)
            fsg = fs_grid.fullgrid(self, self.grid_table)
            fsg.Show()
            del busy
        except Exception, info:
            del busy
            info = str(info)
            info = info.decode('cp1251').encode('utf8')
            wx.MessageBox(info)
            
    def OnAddBtn(self, event):
        if self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[0]:
            self.param = 'no_information'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[1]:
            self.param = 'bad_format'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[2]:
            self.param = 'noise_level'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[3]:
            self.param = 'identifiability'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[4]:
            self.param = 'harmony'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[5]:
            self.param = 'efficiency'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[6]:
            self.param = 'inconsistency'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[7]:
            self.param = 'reliability'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[8]:
            self.param = 'degree_of_classification'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[9]:
            self.param = 'degree_of_structuring'
            
        regexp =  self.edit_regexp_txt.GetValue()
        regexp = str(regexp)
        self.db.add_regexp(self.param, regexp)
        items = self.db.take_regexps(self.param)
        self.regexps_listbox.SetItems(items)
    
    def OnDelBtn(self, event):
        if self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[0]:
            self.param = 'no_information'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[1]:
            self.param = 'bad_format'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[2]:
            self.param = 'noise_level'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[3]:
            self.param = 'identifiability'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[4]:
            self.param = 'harmony'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[5]:
            self.param = 'efficiency'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[6]:
            self.param = 'inconsistency'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[7]:
            self.param = 'reliability'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[8]:
            self.param = 'degree_of_classification'
        elif self.regexp_choice_pull.GetStringSelection() == self.params_regexps_choices[9]:
            self.param = 'degree_of_structuring'
            
        regexp =  self.regexps_listbox.GetStringSelection()
        self.db.del_regexp(self.param, regexp)
        items = self.db.take_regexps(self.param)
        self.regexps_listbox.SetItems(items)
    
    def __del__( self ):
        pass
 

class GridTable(wx.grid.PyGridTableBase):
    def __init__(self, dannie, connection, table):
        wx.grid.PyGridTableBase.__init__(self)
        self.dannie = dannie
        self.table = table
        self.connection = connection
        self.col_names = None
        
    def GetNumberRows(self):
        return len(self.dannie)
        pass
    
    def GetNumberCols(self):
        try:
            return len(self.dannie[0])
        except IndexError, info:
            error = (u"Результат - пустая таблица! %s" % info)
            wx.MessageBox(error)
        pass
    
    def GetColLabelValue(self, col):
        if self.col_names is None:
            try:
                cursor = cx_Oracle.Cursor(self.connection)
                sql = ("select t.COLUMN_ID, t.COLUMN_NAME from all_tab_columns t where t.TABLE_NAME=\'%s\' order by t.COLUMN_ID") % self.table
                cursor.execute(sql)
                cuu=cursor.fetchall()
                cursor.close()
                col_names = [i[1] for i in cuu]
                return col_names [col]
            except (NameError, cx_Oracle.DatabaseError), info:
                info = str(info)
                info = info.decode('cp1251').encode('utf8')
                logging.info(u'Oracle Data Base error:', info)
                error = "Database Error:", info
                wx.MessageBox(error)
        else:
            return col_names[col]
            
    def IsEmptyCell(self, row, col):
        return self.dannie[row] [col] is not None
        pass
    
    def GetValue(self, row, col):
        value = self.dannie[row] [col]
        if value is not None:
            return value
        else:
            value = ' '
            return value
        pass
    
    def SetValue(self, row, col, value):
        self.dannie[row][col]=value
        pass
    
    def CreateGrid(self):
        pass
