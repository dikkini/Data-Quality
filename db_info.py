# -*- coding: utf-8 -*- 

import wx
import sqlite
import string
import logging
import shelve
import os

logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

###########################################################################
## Class dbinfo
###########################################################################

class dbinfo ( wx.Frame ):
    
    def __init__( self, flag, namecon, main ):
        wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Data Quality -- Ввод данных подключения", pos = wx.DefaultPosition, size = wx.Size( 313,351 ), style = wx.CAPTION|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )
        self.main = main
        
        self.wc = work_con()
        self.SetSizeHintsSz( wx.Size( 313,344 ), wx.Size(500,500 ))
        
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_splitter2 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.m_splitter2.SetSashSize( 0 )
        self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )
        
        self.m_panel4 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        fgSizer2 = wx.FlexGridSizer( 1, 2, 0, 20 )
        fgSizer2.SetFlexibleDirection( wx.HORIZONTAL )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )
        
        self.m_staticText9 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Имя соединения:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        fgSizer2.Add( self.m_staticText9, 0, wx.ALL, 5 )
        
        self.name_ctrl = wx.TextCtrl( self.m_panel4,  wx.ID_ANY,  wx.EmptyString, wx.DefaultPosition, wx.Size( 170,-1 ) )
        fgSizer2.Add( self.name_ctrl, 0, wx.ALL, 5 )
        
        self.m_panel4.SetSizer( fgSizer2 )
        self.m_panel4.Layout()
        fgSizer2.Fit( self.m_panel4 )
        self.m_panel5 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sbSizer8 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel5, wx.ID_ANY, u"Свойства соединения" ), wx.VERTICAL )
        
        fgSizer4 = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgSizer4.SetFlexibleDirection( wx.BOTH )
        fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_staticText12 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Имя:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )
        fgSizer4.Add( self.m_staticText12, 0, wx.ALL, 5 )
        
        self.login_ctrl = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 190,-1 ) )
        fgSizer4.Add( self.login_ctrl, 0, wx.ALL, 5 )
        
        self.m_staticText14 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Пароль:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )
        fgSizer4.Add( self.m_staticText14, 0, wx.ALL, 5 )
        
        self.passw_ctrl = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 190,-1 ), wx.TE_PASSWORD )
        fgSizer4.Add( self.passw_ctrl, 0, wx.ALL, 5 )
        
        self.m_staticText18 = wx.StaticText( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText18.Wrap( -1 )
        fgSizer4.Add( self.m_staticText18, 0, wx.ALL, 5 )
        
        self.sv_passw = wx.CheckBox( self.m_panel5, wx.ID_ANY, u"Сохранить пароль?", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer4.Add( self.sv_passw, 0, wx.ALL, 5 )
        
        self.m_staticText19 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"IP адрес:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText19.Wrap( -1 )
        fgSizer4.Add( self.m_staticText19, 0, wx.ALL, 5 )
        
        self.ip_ctrl = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 190,-1 ), 0, Numbers() )
        fgSizer4.Add( self.ip_ctrl, 0, wx.ALL, 5 )
        
        self.m_staticText20 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Порт:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText20.Wrap( -1 )
        fgSizer4.Add( self.m_staticText20, 0, wx.ALL, 5 )
        
        self.port_ctrl = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 190,-1 ), 0, Numbers() )
        fgSizer4.Add( self.port_ctrl, 0, wx.ALL, 5 )
        
        self.sid_radio = wx.RadioButton( self.m_panel5, wx.ID_ANY, u"SID:", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer4.Add( self.sid_radio, 0, wx.ALL, 5 )
        
        self.sid_ctrl = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 190,-1 ) )
        fgSizer4.Add( self.sid_ctrl, 0, wx.ALL, 5 )
        
        self.service_radio = wx.RadioButton( self.m_panel5, wx.ID_ANY, u"Имя сервиса:", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer4.Add( self.service_radio, 0, wx.ALL, 5 )
        
        self.service_ctrl = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 190,-1 ) )
        fgSizer4.Add( self.service_ctrl, 0, wx.ALL, 5 )
        
        self.cancel_btn = wx.Button( self.m_panel5, wx.ID_ANY, u"Выход", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer4.Add( self.cancel_btn, 0, wx.ALL, 5 )
        
        self.ok_btn = wx.Button( self.m_panel5, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer4.Add( self.ok_btn, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        
        sbSizer8.Add( fgSizer4, 1, wx.EXPAND|wx.LEFT, 5 )
        
        self.m_panel5.SetSizer( sbSizer8 )
        self.m_panel5.Layout()
        sbSizer8.Fit( self.m_panel5 )
        self.m_splitter2.SplitHorizontally( self.m_panel4, self.m_panel5, 7 )
        bSizer2.Add( self.m_splitter2, 1, 0, 5 )
        
        self.SetSizer( bSizer2 )
        self.Layout()
        
        self.Centre( wx.BOTH )

        # Working class with BD
        self.sqlite = sqlite.sqliteDB(self.main.schema, self.main.table)
        
        self.ok_btn.Bind( wx.EVT_BUTTON, self.OnOk )
        self.cancel_btn.Bind( wx.EVT_BUTTON, self.OnCancel )
        
        # Choose New or Edit
        self.newcon = flag
        self.namecon = namecon
        if self.newcon is True:
            self.move = True
            logging.info(u'new connection creating')
        elif self.newcon is False:
            self.move = False
            logging.info(u'editing connection: %s' % (namecon))
            dbdata = self.wc.take_data_con(namecon)
            try:
                self.name_ctrl.SetValue(namecon)
                self.ip_ctrl.SetValue(dbdata[0])
                self.port_ctrl.SetValue(dbdata[1])
                self.login_ctrl.SetValue(dbdata[3])
                self.passw_ctrl.SetValue(dbdata[4])
                if dbdata[5] == u'sid':
                    self.sid_radio.SetValue(True)
                    self.sid_ctrl.SetValue(dbdata[2])
                elif dbdata[5] == u'service':
                    self.service_radio.SetValue(True)
                    self.service_ctrl.SetValue(dbdata[2])
            except (IndexError, TypeError), info:
                info = str(info)
                info = info.encode('utf8')
                if "'NoneType' object is not subscriptable" in info:
                    wx.MessageBox(u'Создайте новое подключение!')
                logging.error(u'filling forms connection error:', info)
                self.name_ctrl.SetValue(namecon)

    def m_splitter2OnIdle( self, event ):
        self.m_splitter2.SetSashPosition( 32 )
        self.m_splitter2.Unbind( wx.EVT_IDLE )     
               
    def OnOk(self, event):
        self.name = self.name_ctrl.GetValue()
        self.ip = self.ip_ctrl.GetValue()
        self.port = self.port_ctrl.GetValue()
        self.login = self.login_ctrl.GetValue()
        if len(self.name) == 0:
            wx.MessageBox(u'Поле "Имя соединения" обязательнок заполнению!')
            event.Skip()
            return
        if len(self.ip) == 0:
            wx.MessageBox(u'Поле "IP адрес" обязательно к заполнению!')
            event.Skip()
            return
        if len(self.port) == 0:
            wx.MessageBox(u'Поле "Порт" обязательно к заполнению!')
            event.Skip()
            return
        if len(self.login) == 0:
            wx.MessageBox(u'Поле "Имя" обязательно к заполнению!')
            event.Skip()
            return
            
        if self.sv_passw.GetValue():
            self.passw = self.passw_ctrl.GetValue() 
        else:
            self.passw = wx.EmptyString
        if self.sid_radio.GetValue():
            self.radio = u'sid'
            self.sid = self.sid_ctrl.GetValue()
            self.dbdata = [self.ip, self.port, self.sid, self.login, self.passw, self.radio]
            if self.move is True:
                self.wc.new_con(self.name, self.dbdata)
                self.Close()
            elif self.move is False:
                self.wc.edit_con(self.name, self.dbdata, self.namecon)
                self.Close()
        elif self.service_radio.GetValue():
            self.radio = u'service'
            self.sid = self.service_ctrl.GetValue()
            self.dbdata = [self.ip, self.port, self.sid, self.login, self.passw, self.radio]
            if self.move is True:
                self.wc.new_con(self.name, self.dbdata)
                self.Close()
            elif self.move is False:
                self.wc.edit_con(self.name, self.dbdata, self.namecon)
                self.Close()
        else:
            wx.MessageBox(u'Введите имя сервиса или SID базы данных!')
            
    def OnCancel(self, event):
        self.Destroy()
        

class Numbers(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return Numbers()

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()

        for x in val:
            if x not in string.digits:
                return False

        return True


    def OnChar(self, event):
        key = event.GetKeyCode()
        try:
            # 8 это код клавиши backspace
            if chr(key) in string.digits or chr(key) == '.' or key == 8:
                event.Skip()
            else:
                return False
        except ValueError, info:
            return False
        return     

class AskPassw(wx.Dialog): 
    def __init__(self, connect): 
        wx.Dialog. __init__(self, None, -1, u'Введите пароль для подключения к базе данных',style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.ALWAYS_SHOW_SB|wx.TAB_TRAVERSAL) 
        # Create the text controls 
        passw_txt  = wx.StaticText(self, -1, u"Пароль:")
        # Parent connection 
        self.con = connect
        self.passw_ctrl  = wx.TextCtrl(self, style=wx.TE_PASSWORD)     
        # Use standard button IDs 
        okay   = wx.Button(self, wx.ID_OK) 
        okay.SetDefault() 
        cancel = wx.Button(self, wx.ID_CANCEL) 
        # Layout with sizers 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5) 
        
        fgs = wx.FlexGridSizer(3, 2, 5, 5) 
        fgs.Add(passw_txt, 0, wx.ALIGN_RIGHT) 
        fgs.Add(self.passw_ctrl, 0, wx.EXPAND) 
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
        self.Center()
        
    def OnOk(self, event):
        passw = self.passw_ctrl.GetValue()
        if len(passw) == 0:
            wx.MessageBox(u'Введите пароль!')
        else:
            self.con.dbdata[4] = passw
            self.con.GoConnect()
            self.Close()
            

class work_con():
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__),'data','oracle')
    
    def take_cons(self):
        try:
            #key = str(self.namecon)
            filename = '%s\\connections.dat' % self.path
            d = shelve.open(filename)
            keys = d.keys()
            d.close()
            logging.info(u'list of connections loaded')
            return keys
        except Exception, info:
            info = str(info)
            info = info.encode('utf8')
            logging.error(u'list of connections not loaded')
    
    def new_con(self, namecon, data):
        try:
            key = str(namecon)
            filename = './data/oracle/connections.dat'
            d = shelve.open(filename)
            d[key] = data
            d.sync()
            d.close()
            logging.info(u'new connection %s  created' % (key))
        except Exception, info:
            info = str(info)
            info = info.encode('utf8')
            logging.info(u'new connection was not created')
        
    def edit_con(self, newname, data, namecon):
        try:
            key = str(namecon)
            key2 = str(newname)
            filename = './data/oracle/connections.dat'
            d = shelve.open(filename)
            del d[key]
            d.sync()
            d[key2] = data
            d.sync()
            d.close()
            logging.info(u'editing connection %s successfully: %s' % (namecon, newname))
        except Exception, info:
            namecon = str(namecon)
            namecon = namecon.encode('utf8')
            logging.info(u'editing connection %s failed:', namecon)
    
    def take_data_con(self, namecon):
        try:
            key = str(namecon)
            filename = './data/oracle/connections.dat'
            d = shelve.open(filename)
            data = d[key]
            return data
            logging.info(u'loading data connection %s succesfully' % (namecon))
        except Exception:
            namecon = str(namecon)
            namecon = namecon.encode('utf8')
            logging.error(u'loading data connection %s failed' % (namecon))
        
    def del_con(self, namecon):
        try:
            key = str(namecon)
            filename = './data/oracle/connections.dat'
            d = shelve.open(filename)
            del d[key]
            logging.info(u'delete connection %s succesfully' % (namecon))
        except Exception, info:
            info = str(info)
            info = info.encode('utf8')
            namecon = str(namecon)
            namecon = namecon.encode('utf8')
            logging.error(u'delete connection failed: %s', namecon)
            
        