# -*- coding: utf8 -*-

import wx 
import wx.grid
import sqlite
import cx_Oracle
import fs_grid
import string
import logging
logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

###########################################################################
## Class ParamsChooser
###########################################################################

class frame_chooser ( wx.Frame ):
    
    def __init__(self, parent, schema, table, connection):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u'Выбор параметров для оценки качества данных', pos = wx.DefaultPosition, size = wx.Size( 400,200 ), style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
        
        self.main = parent
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer5 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer6 = wx.BoxSizer( wx.VERTICAL )
        
        self.label1 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Выберите параметры для оценки:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label1.Wrap( -1 )
        bSizer6.Add( self.label1, 0, wx.ALL, 5 )
        
        self.staticline = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer6.Add( self.staticline, 0, wx.EXPAND |wx.ALL, 5 )
        
        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer7.SetMinSize( wx.Size( 100,200 ) ) 
        
        self.params_quality_choices = [u'Пустые значения', u'Не несущие информацию значения', u'Не соответствующие формату значения',
                                        u'Значение уровня шума', u'Идентифицируемость', u'Согласованность', u'Унификация', 
                                        u'Оперативность', u'Противоречивость', u'Степень классификации', 
                                        u'Степень структуризации']
        
        self.params_choice_pull = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 
                                             self.params_quality_choices, 0 )
        bSizer7.Add( self.params_choice_pull, 0, wx.ALL, 5 )
        
        self.use_param_checkbox = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"Использовать параметр", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.use_param_checkbox, 0, wx.ALL, 5 )
        
        
        bSizer6.Add( bSizer7, 1, wx.EXPAND, 5 )
        
        self.label2 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Весовой коэффициент параметра:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label2.Wrap( -1 )
        bSizer6.Add( self.label2, 0, wx.ALL, 5 )
        
        self.weights_txt = wx.TextCtrl( self.m_panel2, validator = WeightsValidator() )
        bSizer6.Add( self.weights_txt, 0, wx.ALL, 5 )
        
        self.OK_btn = wx.Button( self.m_panel2, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.OK_btn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.exit_btn = wx.Button( self.m_panel2, wx.ID_ANY, u"Выход", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.exit_btn, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.m_panel2.SetSizer( bSizer6 )
        self.m_panel2.Layout()
        bSizer6.Fit( self.m_panel2 )
        bSizer5.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        self.use_param_checkbox.Bind(wx.EVT_CHECKBOX, self.OnCheckUseParam)
        self.params_choice_pull.Bind(wx.EVT_CHOICE, self.OnChParamDQ)
        self.Bind(wx.EVT_BUTTON, self.OnConfirmBtn, self.OK_btn)
        self.Bind(wx.EVT_BUTTON, self.OnExitBtn, self.exit_btn)
        
        self.using_params = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.weights_params = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.user_number_catalog = None
        self.user_number_composite_fileds = None
        self.user_number_allfields = None
        self.user_days_can_be = None
        self.incon_fields = None
        #SQLITE
        self.db = sqlite.sqliteDB(self.main.schema, self.main.table)
        
        #Table
        self.table = table
        self.schema = schema
        
        #Connection
        self.connection = connection
 
    def OnExitBtn(self, event):
        self.Close()
    
    def OnConfirmBtn(self, event):
        # Весовые коэффициенты параметров
        self.main.weights = self.weights_params 
        # Используемые параметры
        self.main.using_params = self.using_params
        # Число используемых справочников для параметра Степень классификации
        self.main.user_choice_catalog = self.user_number_catalog
        # Два числа для расчета параметра Степень структуризации - allfields - все поля, composite_fields - составные поля
        self.main.user_number_allfields = self.user_number_allfields
        self.main.user_number_composite_fileds = self.user_number_composite_fileds
        # Число для расчета параметра Оперативность
        self.main.user_days_can_be = self.user_days_can_be
        # ---- Противоречивость
        self.main.incon_fields = self.incon_fields
        self.Close()   

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
                ask = AskEffic(self)
                ask.ShowModal()
            else:
                self.using_params[7] = 0
                self.weights_params[7] = 0
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[8]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[8] = 1
                self.weights_params[8] = self.weights_txt.GetValue()
                param = 'inconsistency'
                ask = AskIncon(self, self.connection, self.table)
                ask.ShowModal()
            else:
                self.using_params[8] = 0
                self.weights_params[8] = 0
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[9]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[9] = 1
                self.weights_params[9] = self.weights_txt.GetValue()
                param = 'degree_of_classification'
                ask = AskCatalogs(self)
                ask.ShowModal()
                
            else:
                self.using_params[9] = 0
                self.weights_params[9] = 0
                
        elif self.params_choice_pull.GetStringSelection() == self.params_quality_choices[10]:
            if self.use_param_checkbox.IsChecked():
                self.using_params[10] = 1
                self.weights_params[10] = self.weights_txt.GetValue()
                param = 'degree_of_structuring'
                ask = AskDoS(self)
                ask.ShowModal()
            else:
                self.using_params[10] = 0
                self.weights_params[10] = 0
    
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

class AskEffic(wx.Dialog): 
    def __init__(self, parent): 
        wx.Dialog. __init__(self, None, -1, u'Укажите пожалуйста допустимое количество дней просроченности данных:',style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.ALWAYS_SHOW_SB|wx.TAB_TRAVERSAL) 
        # Create the text controls 
        txt  = wx.StaticText(self, -1, u"Количество дней:")
        # Parent connection 
        self.par_ch = parent
        self.text_ctrl = wx.TextCtrl(self)     
        # Use standard button IDs 
        okay = wx.Button(self, wx.ID_OK) 
        okay.SetDefault() 
        cancel = wx.Button(self, wx.ID_CANCEL) 
        # Layout with sizers 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5) 
        
        fgs = wx.FlexGridSizer(3, 2, 5, 5) 
        fgs.Add(txt, 0, wx.ALIGN_RIGHT) 
        fgs.Add(self.text_ctrl, 0, wx.EXPAND) 
        fgs.AddGrowableCol(1) 
        sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5) 
        btns = wx.StdDialogButtonSizer() 
        btns.AddButton(okay) 
        btns.AddButton(cancel) 
        btns.Realize() 
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5) 
        self.SetSizer(sizer) 
        sizer.Fit(self)
        okay.Bind(wx.EVT_BUTTON, self.OnOk)
        cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.Center()
        
    def OnOk(self, event):
        value = self.text_ctrl.GetValue()
        if len(value) == 0:
            wx.MessageBox(u'Все поля необходимо заполнить!')
        else:
            self.par_ch.user_days_can_be = value
            self.par_ch.using_params[7] = 1
            self.par_ch.weights_params[7] = 1
            self.par_ch.use_param_checkbox.SetValue(True)
            self.Close()
            
    def OnCancel(self, event):
        self.par_ch.using_params[7] = 0
        self.par_ch.weights_params[7] = 0
        self.par_ch.use_param_checkbox.SetValue(False)
        self.par_ch.weights_txt.Clear()
        self.Close()   

class AskIncon( wx.Dialog ):
    
    def __init__( self, parent, connection, table ):
        wx.Dialog.__init__ ( self, parent=None, id = wx.ID_ANY, title = u'Выбирете пожалуйста уникальные поля таблицы.', style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.ALWAYS_SHOW_SB|wx.TAB_TRAVERSAL )
        
        self.par_ch = parent 
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        #self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        import oracle
        orcl = oracle.WorkDB(connection)
        choice_fieldsChoices = orcl.get_cols(table)
        self.choice_fields = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_fieldsChoices, 0 )
        self.choice_fields.SetSelection( 0 )
        bSizer2.Add( self.choice_fields, 0, wx.ALL, 5 )
        
        self.check_field = wx.CheckBox( self, wx.ID_ANY, u"Для заполнения данного поля использовался справочник!", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.check_field, 0, wx.ALL, 5 )
        
        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.ok_btn = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.ok_btn, 0, wx.ALL, 5 )
        
        self.exit_btn = wx.Button( self, wx.ID_ANY, u"Выход", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.exit_btn, 0, wx.ALL, 5 )
        
        
        bSizer2.Add( bSizer8, 1, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer2 )
        self.Layout()
        #bSizer2.Fit( self.m_panel1 )
        #bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        self.ok_btn.Bind(wx.EVT_BUTTON, self.OnOk)
        self.exit_btn.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.check_field.Bind(wx.EVT_CHECKBOX, self.OnCheck)
        self.choice_fields.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        #vars
        self.list_of_fields = []
        
    def OnChoice(self, event):
        choiced = self.choice_fields.GetStringSelection()
        if choiced in self.list_of_fields:
            self.check_field.SetValue(True)
        else:
            self.check_field.SetValue(False)
        
    def OnCheck(self, event):
        field = self.choice_fields.GetStringSelection()
        if field in self.list_of_fields:
            self.list_of_fields.remove(field)
            self.check_field.SetValue(False)
        else:
            self.list_of_fields.append(field)
        
    def OnOk(self, event):
        if len(self.list_of_fields) == 0:
            wx.MessageBox(u'Необходимо выбрать хотя бы одно поле!')
        else:
            self.par_ch.incon_fields = self.list_of_fields
            self.par_ch.using_params[8] = 1
            self.par_ch.weights_params[8] = 1
            self.par_ch.use_param_checkbox.SetValue(True)
            self.Close()
            
    def OnCancel(self, event):
        self.par_ch.using_params[8] = 0
        self.par_ch.weights_params[8] = 0
        self.par_ch.use_param_checkbox.SetValue(False)
        self.par_ch.weights_txt.Clear()
        self.Close()   

    
    def __del__( self ):
        pass
    



class AskCatalogs(wx.Dialog): 
    def __init__(self, parent): 
        wx.Dialog. __init__(self, None, -1, u'Укажите пожалуйста Количество справочников использовавшееся для заполнения таблицы:',style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.ALWAYS_SHOW_SB|wx.TAB_TRAVERSAL) 
        # Create the text controls 
        txt  = wx.StaticText(self, -1, u"Количество справочников:")
        # Parent connection 
        self.par_ch = parent
        self.text_ctrl = wx.TextCtrl(self)     
        # Use standard button IDs 
        okay = wx.Button(self, wx.ID_OK) 
        okay.SetDefault() 
        cancel = wx.Button(self, wx.ID_CANCEL) 
        # Layout with sizers 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5) 
        
        fgs = wx.FlexGridSizer(3, 2, 5, 5) 
        fgs.Add(txt, 0, wx.ALIGN_RIGHT) 
        fgs.Add(self.text_ctrl, 0, wx.EXPAND) 
        fgs.AddGrowableCol(1) 
        sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5) 
        btns = wx.StdDialogButtonSizer() 
        btns.AddButton(okay) 
        btns.AddButton(cancel) 
        btns.Realize() 
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5) 
        self.SetSizer(sizer) 
        sizer.Fit(self)
        okay.Bind(wx.EVT_BUTTON, self.OnOk)
        cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.Center()
        
    def OnOk(self, event):
        value = self.text_ctrl.GetValue()
        if len(value) == 0:
            wx.MessageBox(u'Все поля необходимо заполнить!')
        else:
            self.par_ch.user_number_catalog = value
            self.par_ch.using_params[9] = 1
            self.par_ch.weights_params[9] = 1
            self.par_ch.use_param_checkbox.SetValue(True)
            self.Close()
    
    def OnCancel(self, event):
        self.par_ch.using_params[9] = 0
        self.par_ch.weights_params[9] = 0
        self.par_ch.use_param_checkbox.SetValue(False)
        self.par_ch.weights_txt.Clear()
        self.Close()
        
class AskDoS(wx.Dialog): 
    def __init__(self, parent): 
        wx.Dialog. __init__(self, None, -1, u'Укажите пожалуйста входные данные для параметра:',style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.ALWAYS_SHOW_SB|wx.TAB_TRAVERSAL) 
        # Create the text controls 
        txt1  = wx.StaticText(self, -1, u"Количество всех полей:")
        txt2  = wx.StaticText(self, -1, u"Количество составных полей:")
        # Parent connection 
        self.par_ch = parent
        self.text1_ctrl = wx.TextCtrl(self)
        self.text2_ctrl = wx.TextCtrl(self)     
        # Use standard button IDs 
        okay = wx.Button(self, wx.ID_OK) 
        okay.SetDefault() 
        cancel = wx.Button(self, wx.ID_CANCEL) 
        # Layout with sizers 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        sizer.Add(txt1, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(txt2, 0, wx.EXPAND|wx.ALL, 5)  
        
        fgs = wx.FlexGridSizer(3, 2, 5, 5) 
        fgs.Add(txt1, 0, wx.ALIGN_RIGHT)
        fgs.Add(txt2, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.text1_ctrl, 0, wx.EXPAND)
        fgs.Add(self.text2_ctrl, 0, wx.EXPAND) 
        fgs.AddGrowableCol(1) 
        sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5) 
        btns = wx.StdDialogButtonSizer() 
        btns.AddButton(okay) 
        btns.AddButton(cancel) 
        btns.Realize() 
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5) 
        self.SetSizer(sizer) 
        sizer.Fit(self)
        okay.Bind(wx.EVT_BUTTON, self.OnOk)
        cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.Center()
        
    def OnOk(self, event):
        allfields = self.text1_ctrl.GetValue()
        composite_fileds = self.text2_ctrl.GetValue()
        if len(allfields) == 0 or len(composite_fileds) == 0:
            wx.MessageBox(u'Все поля необходимо заполнить!')
        else:
            self.par_ch.user_number_allfields = allfields
            self.par_ch.user_number_composite_fileds = composite_fileds
            self.par_ch.using_params[10] = 1
            self.par_ch.weights_params[10] = 1
            self.par_ch.use_param_checkbox.SetValue(True)
            self.Close()
    
    def OnCancel(self, event):
        self.par_ch.using_params[10] = 0
        self.par_ch.weights_params[10] = 0
        self.par_ch.use_param_checkbox.SetValue(False)
        self.par_ch.weights_txt.Clear()        
        self.Close()

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
            return False
        return   