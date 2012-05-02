# -*- coding: utf-8 -*- 

import wx
import sqlite
import db_info
import cx_Oracle
import logging
logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

###########################################################################
## Class connections
###########################################################################

class connections ( wx.Frame ):
    
    def __init__( self, main ):
        wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Data Quality -- Подключение к базе данных", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.ALWAYS_SHOW_SB|wx.TAB_TRAVERSAL )
        
        
        # temp var
        #self.namecon = None
        self.main = main
        
        
        self.wc = db_info.work_con()
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_splitter3 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_splitter3.Bind( wx.EVT_IDLE, self.m_splitter3OnIdle )
        
        self.m_panel1 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,100 ), wx.TAB_TRAVERSAL )
        
        fgSizer6 = wx.FlexGridSizer( 1, 1, 0, 0 )
        fgSizer6.SetFlexibleDirection( wx.BOTH )
        fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_staticText17 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Выберете соединение с базой данных", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText17.Wrap( -1 )
        fgSizer6.Add( self.m_staticText17, 0, wx.ALL, 5 )
        
        self.m_panel1.SetSizer( fgSizer6 )
        self.m_panel1.Layout()
        self.m_panel2 = wx.Panel( self.m_splitter3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        fgSizer7 = wx.FlexGridSizer( 2, 3, 0, 0 )
        fgSizer7.SetFlexibleDirection( wx.BOTH )
        fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_staticText18 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Соединения с базой данных:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText18.Wrap( -1 )
        fgSizer7.Add( self.m_staticText18, 0, wx.ALL, 5 )
        
        # Получаем список коннектов
        items = self.wc.take_cons()
        self.connections_choice = wx.Choice( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, items, 0 )
        
        self.connections_choice.SetSelection( 0 )
        fgSizer7.Add( self.connections_choice, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.m_panel2.SetSizer( fgSizer7 )
        self.m_panel2.Layout()
        fgSizer7.Fit( self.m_panel2 )
        self.m_splitter3.SplitHorizontally( self.m_panel1, self.m_panel2, 29 )
        bSizer3.Add( self.m_splitter3, 1, wx.EXPAND, 5 )
        
        self.m_splitter5 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_splitter5.Bind( wx.EVT_IDLE, self.m_splitter5OnIdle )
        
        self.m_panel3 = wx.Panel( self.m_splitter5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        fgSizer9 = wx.FlexGridSizer( 2, 3, 0, 0 )
        fgSizer9.SetFlexibleDirection( wx.BOTH )
        fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.newcon_btn = wx.Button( self.m_panel3, wx.ID_ANY, u"Новое соединение", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        fgSizer9.Add( self.newcon_btn, 0, wx.ALL, 5 )
        
        self.editcon_btn = wx.Button( self.m_panel3, wx.ID_ANY, u"Редактировать", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        fgSizer9.Add( self.editcon_btn, 0, wx.ALL, 5 )
        
        self.delcon_btn = wx.Button( self.m_panel3, wx.ID_ANY, u"Удалить", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        fgSizer9.Add( self.delcon_btn, 0, wx.ALL, 5 )
        
        self.m_panel3.SetSizer( fgSizer9 )
        self.m_panel3.Layout()
        fgSizer9.Fit( self.m_panel3 )
        self.m_panel20 = wx.Panel( self.m_splitter5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer12 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_splitter10 = wx.SplitterWindow( self.m_panel20, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_splitter10.Bind( wx.EVT_IDLE, self.m_splitter10OnIdle )
        
        self.m_panel21 = wx.Panel( self.m_splitter10, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer8 = wx.GridSizer( 1, 3, 0, 0 )
        
        self.help_btn = wx.Button( self.m_panel21, wx.ID_ANY, u"Помощь", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer8.Add( self.help_btn, 0, wx.ALL, 5 )
        
        self.ok_btn = wx.Button( self.m_panel21, wx.ID_ANY, u"Соединится", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer8.Add( self.ok_btn, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        
        self.cancel_btn = wx.Button( self.m_panel21, wx.ID_ANY, u"Отмена", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer8.Add( self.cancel_btn, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        
        self.m_panel21.SetSizer( gSizer8 )
        self.m_panel21.Layout()
        gSizer8.Fit( self.m_panel21 )
        self.m_splitter10.Initialize( self.m_panel21 )
        bSizer12.Add( self.m_splitter10, 1, wx.EXPAND, 5 )
        
        self.m_panel20.SetSizer( bSizer12 )
        self.m_panel20.Layout()
        bSizer12.Fit( self.m_panel20 )
        self.m_splitter5.SplitHorizontally( self.m_panel3, self.m_panel20, 0 )
        bSizer3.Add( self.m_splitter5, 1, wx.EXPAND, 5 )
        
        self.SetSizer( bSizer3 )
        self.Layout()
        bSizer3.Fit( self )
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.connections_choice.Bind( wx.EVT_CHOICE, self.OnChoiceCon )
        self.newcon_btn.Bind( wx.EVT_BUTTON, self.OnNewCon )
        self.editcon_btn.Bind( wx.EVT_BUTTON, self.OnEditCon )
        self.delcon_btn.Bind( wx.EVT_BUTTON, self.OnDelCon )
        self.help_btn.Bind( wx.EVT_BUTTON, self.OnHelp )
        self.ok_btn.Bind( wx.EVT_BUTTON, self.OnOk )
        self.cancel_btn.Bind( wx.EVT_BUTTON, self.OnCancel )
        self.Bind( wx.EVT_ACTIVATE, self.OnInit )

    def OnInit(self, event):
        try:
            items = self.wc.take_cons()
            self.connections_choice.SetItems(items)
            self.connections_choice.SetSelection( 0 )
            namecon = self.connections_choice.GetStringSelection()
            self.dbdata = self.wc.take_data_con(namecon)
            event.Skip()
            logging.info(u'listing of conneciton succesfully loading')
        except wx._core.PyDeadObjectError, info:
            info = str(info)
            info = info.encode('utf8')
            logging.error(u'exit programm with code 0 before close all windows: %s' % info)

            return
        
    def OnChoiceCon( self, event ):
        if not namecon:
            namecon = 'none'
        namecon = self.connections_choice.GetStringSelection()
        if not namecon:
            namecon = 'none'
            event.Skip()
            return
        self.dbdata = self.wc.take_data_con(namecon)
        logging.info(u'trying to connect using conneciton: %s' % (namecon))
        
    def OnNewCon( self, event ):
        flag = True
        #namecon = self.connections_choice.GetStringSelection()
        namecon = None
        editcon = db_info.dbinfo(flag, namecon, self.main)
        editcon.Show()
        logging.info(u'creating new connection')
        
    def OnEditCon( self, event ):
        flag = False
        namecon = self.connections_choice.GetStringSelection()
        if not namecon:
            wx.MessageBox(u'Создайте новое соединение!')
            event.Skip()
            return
        editcon = db_info.dbinfo(flag, namecon, self.main)
        editcon.Show()
        logging.info(u'editing connection: %s' % (namecon))
    
    def OnDelCon( self, event ):
        namecon = self.connections_choice.GetStringSelection()
        self.wc.del_con(namecon)
        items = self.wc.take_cons()
        self.connections_choice.SetItems(items)
        logging.info(u'try to delete connection: %s' % (namecon))
        
    def OnHelp( self, event ):
        event.Skip()
    
    def OnOk( self, event ):
        if not self.dbdata:
            wx.MessageBox(u'Создайте новое соединение!')
            event.Skip()
            return
        if self.dbdata[4] == wx.EmptyString:
            passw = db_info.AskPassw(self)
            passw.ShowModal()
            logging.info(u'trying connection to db')
        else:
            self.GoConnect()
       
    def GoConnect( self ):
        try:
            self.dsn_tns = cx_Oracle.makedsn(self.dbdata[0], self.dbdata[1], self.dbdata[2])
            self.connection = cx_Oracle.connect(self.dbdata[3], self.dbdata[4], self.dsn_tns)
            #Enable main menubar elements
            self.main.connection = self.connection
            self.main.statusbar.SetStatusText(u'Выполнено подключение к базе')
            self.main.BD.Enable(1, False)
            self.main.BD.Enable(2, True)
            #self.main.DQ.Enable(4, True)
            #self.main.DQ.Enable(5, True)
            #self.main.regexp.Enable(6, True)
            #self.main.regexp.Enable(7, True)
            #self.main.logs.Enable(8, True)
            #self.main.logs.Enable(9, True)
            logging.info(u'connection to database. info: %s, %s, %s, %s' % (self.dbdata[0], self.dbdata[1], self.dbdata[2], self.dbdata[3]))
            # Check ENCODING DATABASE
            dbenc = self.connection.encoding
            if dbenc != 'WINDOWS-1251':
                wx.MessageBox(u'Не верная кодировка базы данных. Обратитесь к системному администратору.')
            self.Close()        
            
        except (cx_Oracle.DatabaseError, cx_Oracle.DataError, AttributeError), info:
            error = u'Не возможно подключиться к базе данных. Проверьте правильность введенных данных.'
            wx.MessageBox(error)
            info = str(info)
            info = info.decode('cp1251').encode('utf8')
            logging.error(u'connection error: %s' % info)
            self.Close()
            
    def OnCancel( self, event ):
        self.Destroy()
    
    def m_splitter3OnIdle( self, event ):
        self.m_splitter3.SetSashPosition( 29 )
        self.m_splitter3.Unbind( wx.EVT_IDLE )
    
    def m_splitter5OnIdle( self, event ):
        self.m_splitter5.SetSashPosition( 0 )
        self.m_splitter5.Unbind( wx.EVT_IDLE )
    
    def m_splitter10OnIdle( self, event ):
        self.m_splitter10.SetSashPosition( 0 )
        self.m_splitter10.Unbind( wx.EVT_IDLE )