# -*- coding: utf8 -*-
import wx #@UnusedImport
import wx.grid
import sqlite
import cx_Oracle
import fs_grid
import string
import logging
logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

###########################################################################
## Class regexps
###########################################################################

class regexps ( wx.Frame ):
    
    def __init__( self, main, schema, table, connection ):
        wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Data Quality -- Выбор и отладка регулярных выражений", 
                            pos = wx.DefaultPosition, size = wx.Size( 510,477 ), style = wx.CAPTION|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        sizer1 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.regexps_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.dq_params_tab = wx.Panel( self.regexps_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer2 = wx.BoxSizer( wx.VERTICAL )
        
        sizer2.SetMinSize( wx.Size( 2,2 ) ) 
        self.use_param_checkbox = wx.CheckBox( self.dq_params_tab, wx.ID_ANY, u"Использовать параметр", wx.DefaultPosition, 
                                               wx.DefaultSize, 0 )
        sizer2.Add( self.use_param_checkbox, 0, wx.ALL, 5 )
        
        self.params_quality_choices = [u'Пустые значения', u'Не несущие информацию значения', u'Не соответствующие формату значения',
                                        u'Значение уровня шума', u'Идентифицируемость', u'Согласованность', u'Унификация', 
                                        u'Оперативность', u'Противоречивость', u'Достоверность', u'Степень классификации', 
                                        u'Степень структуризации']
        
        self.params_choice_pull = wx.Choice( self.dq_params_tab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 
                                             self.params_quality_choices, 0 )
        self.params_choice_pull.SetSelection( 0 )
        sizer2.Add( self.params_choice_pull, 0, wx.ALL, 5 )
        
        self.static_line = wx.StaticLine( self.dq_params_tab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        sizer2.Add( self.static_line, 0, wx.EXPAND |wx.ALL, 5 )
        
        self.static_text = wx.StaticText( self.dq_params_tab, wx.ID_ANY, u"Ввод весового коэффициента", wx.DefaultPosition, 
                                          wx.DefaultSize, 0 )
        self.static_text.Wrap( -1 )
        sizer2.Add( self.static_text, 0, wx.ALL, 5 )
        
        self.weights_txt = wx.TextCtrl( self.dq_params_tab, validator = WeightsValidator() )
        sizer2.Add( self.weights_txt, 0, wx.ALL, 5 )
        
        self.OK_btn = wx.Button( self.dq_params_tab, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer2.Add( self.OK_btn, 0, wx.ALL, 5 )
        
        self.dq_params_tab.SetSizer( sizer2 )
        self.dq_params_tab.Layout()
        sizer2.Fit( self.dq_params_tab )
        self.regexps_notebook.AddPage( self.dq_params_tab, u"Параметры оценки", False )
        self.regexps_tab = wx.Panel( self.regexps_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer3 = wx.BoxSizer( wx.VERTICAL )
        
        self.static_text9 = wx.StaticText( self.regexps_tab, wx.ID_ANY, u"Список критериев", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.static_text9.Wrap( -1 )
        sizer3.Add( self.static_text9, 0, wx.ALL, 5 )
        
        self.params_regexps_choices = [u'Не несущие информацию значения', u'Не соответствующие формату значения', 
                                       u'Значение уровня шума', u'Идентифицируемость', u'Согласованность', u'Оперативность', 
                                       u'Противоречивость', u'Достоверность', u'Степень классификации', u'Степень структуризации']
        
        self.regexp_choice_pull = wx.Choice( self.regexps_tab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 
                                             self.params_regexps_choices, 0 )
        self.regexp_choice_pull.SetSelection( 0 )
        sizer3.Add( self.regexp_choice_pull, 0, wx.ALL|wx.EXPAND, 5 )
        
        regexps_listboxChoices = []
        self.regexps_listbox = wx.ListBox( self.regexps_tab, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 
                                           regexps_listboxChoices, wx.LB_HSCROLL|wx.LB_SINGLE )
        sizer3.Add( self.regexps_listbox, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.m_staticText10 = wx.StaticText( self.regexps_tab, wx.ID_ANY, u"Поле для ввода/редактирования регулярного выражения", 
                                             wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        sizer3.Add( self.m_staticText10, 0, wx.ALL, 5 )
        
        self.edit_regexp_txt = wx.TextCtrl( self.regexps_tab, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 465,50 ), 0 )
        sizer3.Add( self.edit_regexp_txt, 0, wx.ALL, 5 )
        
        self.add_regexp_btn = wx.Button( self.regexps_tab, wx.ID_ANY, u"Добавить", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer3.Add( self.add_regexp_btn, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.del_regexp_btn = wx.Button( self.regexps_tab, wx.ID_ANY, u"Удалить", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer3.Add( self.del_regexp_btn, 0, wx.ALL|wx.ALIGN_RIGHT|wx.EXPAND, 5 )
        
        self.checksql_btn = wx.Button( self.regexps_tab, wx.ID_ANY, u"Проверка синтаксиса SQL", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer3.Add( self.checksql_btn, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.exit_btn = wx.Button( self.regexps_tab, wx.ID_ANY, u"Выход", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer3.Add( self.exit_btn, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.regexps_tab.SetSizer( sizer3 )
        self.regexps_tab.Layout()
        sizer3.Fit( self.regexps_tab )
        self.regexps_notebook.AddPage( self.regexps_tab, u"Ввод регулярных выражений", True )
        #self.check_sql_tab = wx.Panel( self.regexps_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer4 = wx.BoxSizer( wx.VERTICAL )
        
        #Вкладка с маленьким гридом, на при этом багает большой грид. Есть мысля переиначить интерфейс модуля редактирования регулярных выражений.
        #=======================================================================
        # self.check_grid = wx.grid.Grid( self.check_sql_tab, wx.ID_ANY, wx.DefaultPosition, wx.Size(480,407), wx.HSCROLL|wx.VSCROLL )
        # 
        # # Grid
        # self.check_grid.CreateGrid( 5, 5 )
        # self.check_grid.EnableEditing( False )
        # self.check_grid.EnableGridLines( True )
        # self.check_grid.EnableDragGridSize( False )
        # self.check_grid.SetMargins( 0, 0 )
        # 
        # # Columns
        # self.check_grid.EnableDragColMove( False )
        # self.check_grid.EnableDragColSize( False )
        # self.check_grid.SetColLabelSize( 20 )
        # self.check_grid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        # 
        # # Rows
        # self.check_grid.AutoSizeRows( True )
        # self.check_grid.EnableDragRowSize( True )
        # self.check_grid.SetRowLabelSize( 40 )
        # self.check_grid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        # 
        # # Label Appearance
        # 
        # # Cell Defaults
        # self.check_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        # sizer4.Add( self.check_grid, 0, wx.ALL, 5 )
        #=======================================================================
        
        #=======================================================================
        # self.check_sql_tab.SetSizer( sizer4 )
        # self.check_sql_tab.Layout()
        # sizer4.Fit( self.check_sql_tab )
        # self.regexps_notebook.AddPage( self.check_sql_tab, u"Проверка регулярных выражений", False )
        #=======================================================================
        
        sizer1.Add( self.regexps_notebook, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.SetSizer( sizer1 )
        self.Layout()
        self.Centre( wx.BOTH )
        
        # Binds Events
        self.use_param_checkbox.Bind(wx.EVT_CHECKBOX, self.OnCheckUseParam)
        self.regexps_listbox.Bind(wx.EVT_LISTBOX_DCLICK, self.OnChRegexp)
        self.params_choice_pull.Bind(wx.EVT_CHOICE, self.OnChParamDQ)
        self.regexp_choice_pull.Bind(wx.EVT_CHOICE, self.OnChParamRegexp)
        self.edit_regexp_txt.Bind(wx.EVT_TEXT, self.OnEditRegexp)
        #self.check_sql_tab.Bind( wx.EVT_LEFT_DCLICK, self.OnGridTab)
                                        
        #Events Buttons
        self.Bind(wx.EVT_BUTTON, self.OnTestBtn, self.checksql_btn)
        self.Bind(wx.EVT_BUTTON, self.OnAddBtn, self.add_regexp_btn)
        self.Bind(wx.EVT_BUTTON, self.OnDelBtn, self.del_regexp_btn)
        self.Bind(wx.EVT_BUTTON, self.OnConfirmBtn, self.OK_btn)
        self.Bind(wx.EVT_BUTTON, self.OnExitBtn, self.exit_btn)
        
        # Variables
        self.using_params = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.weights_params = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.main = main
        
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
            
    def OnCheckUseParam(self, event):
        try:
            if self.weights_txt.GetValue() == wx.EmptyString or self.weights_txt.GetValue() in string.punctuation or float(self.weights_txt.GetValue()) > 1 or self.weights_txt.GetValue() == '0':
                wx.MessageBox(u'Введен не верный весовой коэффициент. За описанием обратитесь в справку.')
                self.use_param_checkbox.SetValue( False )
                event.Skip()
        except ValueError:
            wx.MessageBox(u'Введен не верный весовой коэффициент. За описанием обратитесь в справку.')
            self.use_param_checkbox.SetValue( False )
            event.Skip()
        if self.params_choice_pull.GetStringSelection() == self.params_quality_choices[0]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[0] = 1
                self.weights_params[0] = self.weights_txt.GetValue()
            else:
                self.using_params[0] = 0
                self.weights_params[0] = 0
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[1]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[1] = 1
                self.weights_params[1] = self.weights_txt.GetValue()
                param = 'no_information'
                test = self.db.take_regexps(param)
                if not test:
                    wx.MessageBox(u'Для данного параметра не введены регулярные выражения.')
                    self.using_params[1] = 0
                    self.weights_params[1] = 0
                    self.use_param_checkbox.SetValue(False)
                    self.weights_txt.Clear()
            else:
                self.using_params[1] = 0
                self.weights_params[1] = 0
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[2]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[2] = 1
                self.weights_params[2] = self.weights_txt.GetValue()
                param = 'bad_format'
                test = self.db.take_regexps(param)
                if not test:
                    wx.MessageBox(u'Для данного параметра не введены регулярные выражения.')
                    self.using_params[2] = 0
                    self.weights_params[2] = 0
                    self.use_param_checkbox.SetValue(False)
                    self.weights_txt.Clear()
            else:
                self.using_params[2] = 0
                self.weights_params[2] = 0
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[3]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[3] = 1
                self.weights_params[3] = self.weights_txt.GetValue()
                param = 'noise_level'
                test = self.db.take_regexps(param)
                if not test:
                    wx.MessageBox(u'Для данного параметра не введены регулярные выражения.')
                    self.using_params[3] = 0
                    self.weights_params[3] = 0
                    self.use_param_checkbox.SetValue(False)
                    self.weights_txt.Clear()
            else:
                self.using_params[3] = 0
                self.weights_params[3] = 0
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[4]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[4] = 1
                self.weights_params[4] = self.weights_txt.GetValue()
                param = 'identifiability'
                test = self.db.take_regexps(param)
                if not test:
                    wx.MessageBox(u'Для данного параметра не введены регулярные выражения.')
                    self.using_params[4] = 0
                    self.weights_params[4] = 0
                    self.use_param_checkbox.SetValue(False)
                    self.weights_txt.Clear()
            else:
                self.using_params[4] = 0
                self.weights_params[4] = 0
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[5]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[5] = 1
                self.weights_params[5] = self.weights_txt.GetValue()
                param = 'harmony'
                test = self.db.take_regexps(param)
                if not test:
                    wx.MessageBox(u'Для данного параметра не введены регулярные выражения.')
                    self.using_params[5] = 0
                    self.weights_params[5] = 0
                    self.use_param_checkbox.SetValue(False)
                    self.weights_txt.Clear()
            else:
                self.using_params[5] = 0
                self.weights_params[5] = 0
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[6]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[6] = 1
                self.weights_params[6] = self.weights_txt.GetValue()
            else:
                self.using_params[6] = 0
                self.weights_params[6] = 0
                
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[7]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[7] = 1
                self.weights_params[7] = self.weights_txt.GetValue()
                param = 'efficiency'
                test = self.db.take_regexps(param)
                if not test:
                    wx.MessageBox(u'Для данного параметра не введены регулярные выражения.')
                    self.using_params[7] = 0
                    self.weights_params[7] = 0
                    self.use_param_checkbox.SetValue(False)
                    self.weights_txt.Clear()
            else:
                self.using_params[7] = 0
                self.weights_params[7] = 0
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[8]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[8] = 1
                self.weights_params[8] = self.weights_txt.GetValue()
                param = 'inconsistency'
                test = self.db.take_regexps(param)
                if not test:
                    wx.MessageBox(u'Для данного параметра не введены регулярные выражения.')
                    self.using_params[8] = 0
                    self.weights_params[8] = 0
                    self.use_param_checkbox.SetValue(False)
                    self.weights_txt.Clear()
            else:
                self.using_params[8] = 0
                self.weights_params[8] = 0
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[9]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[9] = 1
                self.weights_params[9] = self.weights_txt.GetValue()
                param = 'reliability'
                test = self.db.take_regexps(param)
                if not test:
                    wx.MessageBox(u'Для данного параметра не введены регулярные выражения.')
                    self.using_params[9] = 0
                    self.weights_params[9] = 0
                    self.use_param_checkbox.SetValue(False)
                    self.weights_txt.Clear()
            else:
                self.using_params[9] = 0
                self.weights_params[9] = 0
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[10]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[10] = 1
                self.weights_params[10] = self.weights_txt.GetValue()
                param = 'degree_of_classification'
                test = self.db.take_regexps(param)
                if not test:
                    wx.MessageBox(u'Для данного параметра не введены регулярные выражения.')
                    self.using_params[10] = 0
                    self.weights_params[10] = 0
                    self.use_param_checkbox.SetValue(False)
                    self.weights_txt.Clear()
            else:
                self.using_params[10] = 0
                self.weights_params[10] = 0
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[11]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[11] = 1
                self.weights_params[11] = self.weights_txt.GetValue()
                param = 'degree_of_structuring'
                test = self.db.take_regexps(param)
                if not test:
                    wx.MessageBox(u'Для данного параметра не введены регулярные выражения.')
                    self.using_params[11] = 0
                    self.weights_params[11] = 0
                    self.use_param_checkbox.SetValue(False)
                    self.weights_txt.Clear()
            else:
                self.using_params[11] = 0
                self.weights_params[11] = 0
    
    def OnChParamDQ(self, event):
        if self.params_choice_pull.GetStringSelection() == self.params_quality_choices[0]:
            if self.using_params[0] == 1:
                self.use_param_checkbox.SetValue(True)
                self.weights_txt.SetValue(self.weights_params[0])
            else:
                self.use_param_checkbox.SetValue(False)
                self.weights_txt.Clear()
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[1]:
            if self.using_params[1] == 1:
                self.use_param_checkbox.SetValue(True)
                self.weights_txt.SetValue(self.weights_params[1])
            else:
                self.use_param_checkbox.SetValue(False)
                self.weights_txt.Clear()
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[2]:
            if self.using_params[2] == 1:
                self.use_param_checkbox.SetValue(True)
                self.weights_txt.SetValue(self.weights_params[2])
            else:
                self.use_param_checkbox.SetValue(False)
                self.weights_txt.Clear()
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[3]:
            if self.using_params[3] == 1:
                self.use_param_checkbox.SetValue(True)
                self.weights_txt.SetValue(self.weights_params[3])
            else:
                self.use_param_checkbox.SetValue(False)
                self.weights_txt.Clear()
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[4]:
            if self.using_params[4] == 1:
                self.use_param_checkbox.SetValue(True)
                self.weights_txt.SetValue(self.weights_params[4])
            else:
                self.use_param_checkbox.SetValue(False)
                self.weights_txt.Clear()
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[5]:
            if self.using_params[5] == 1:
                self.use_param_checkbox.SetValue(True)
                self.weights_txt.SetValue(self.weights_params[5])
            else:
                self.use_param_checkbox.SetValue(False)
                self.weights_txt.Clear()
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[6]:
            if self.using_params[6] == 1:
                self.use_param_checkbox.SetValue(True)
                self.weights_txt.SetValue(self.weights_params[6])
            else:
                self.use_param_checkbox.SetValue(False)
                self.weights_txt.Clear()
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[7]:
            if self.using_params[7] == 1:
                self.use_param_checkbox.SetValue(True)
                self.weights_txt.SetValue(self.weights_params[7])
            else:
                self.use_param_checkbox.SetValue(False)
                self.weights_txt.Clear()
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[8]:
            if self.using_params[8] == 1:
                self.use_param_checkbox.SetValue(True)
                self.weights_txt.SetValue(self.weights_params[8])
            else:
                self.use_param_checkbox.SetValue(False)
                self.weights_txt.Clear()
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[9]:
            if self.using_params[9] == 1:
                self.use_param_checkbox.SetValue(True)
                self.weights_txt.SetValue(self.weights_params[9])
            else:
                self.use_param_checkbox.SetValue(False)
                self.weights_txt.Clear()
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[10]:
            if self.using_params[10] == 1:
                self.use_param_checkbox.SetValue(True)
                self.weights_txt.SetValue(self.weights_params[10])
            else:
                self.use_param_checkbox.SetValue(False)
                self.weights_txt.Clear()
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[11]:
            if self.using_params[11] == 1:
                self.use_param_checkbox.SetValue(True)
                self.weights_txt.SetValue(self.weights_params[11])
            else:
                self.use_param_checkbox.SetValue(False)
                self.weights_txt.Clear()
    
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
        try:
            cursor = cx_Oracle.Cursor(self.connection)
            regexp = self.edit_regexp_txt.GetValue()
            sql = ('select * from %s.%s where %s') % (self.schema, self.table, regexp)
            cursor.execute(sql)
            grid_data=cursor.fetchall()
            data = []
            for item in grid_data:
                data.append(map(lambda a: a.decode('cp1251') if isinstance(a, basestring) else a, item))
            self.grid_table = GridTable(data, self.connection, self.table)
            cursor.close()
            #self.check_grid.SetTable(self.grid_table, True)
            fsg = fs_grid.fullgrid(self.grid_table)
            fsg.Show()
            self.check_grid.AutoSizeColumns( True )
        except Exception, info:
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
        
    def OnConfirmBtn(self, event):
        self.main.weights = self.weights_params
        self.main.using_params = self.using_params
        print self.using_params
        self.Close()
        
    def OnExitBtn(self, event):
        self.Close()
    
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


class WeightsValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return WeightsValidator()

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()

        for x in val:
            if x not in string.digits:
                return False
            
        
        return True

    def OnChar(self, event):
        key = event.GetKeyCode()
        try:                                             # 8 это код клавиши backspace
            if chr(key) in string.digits or chr(key) == '.' or key == 8:
                event.Skip()
            else:
                return False
        except ValueError, info:
            print info
            return False
        return     
