# -*- coding: utf-8 -*- 

import wx
import oracle
import logging
logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class choose_table ( wx.Dialog ):
    
    def __init__( self, connection, parentMain):
        wx.Dialog.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Data Quality -- Выбор таблицы", pos = wx.DefaultPosition, size = wx.Size( 245,217 ), style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.ALWAYS_SHOW_SB )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.schema_txt = wx.StaticText( self.panel, wx.ID_ANY, u"Выбор схемы:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.schema_txt.Wrap( -1 )
        bSizer2.Add( self.schema_txt, 0, wx.ALL, 5 )
        
        choice_schemaChoices = []
        self.choice_schema = wx.Choice( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_schemaChoices, 0 )
        self.choice_schema.SetSelection( 0 )
        bSizer2.Add( self.choice_schema, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.table_txt = wx.StaticText( self.panel, wx.ID_ANY, u"Выбор таблицы:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.table_txt.Wrap( -1 )
        bSizer2.Add( self.table_txt, 0, wx.ALL, 5 )
        
        choice_tableChoices = []
        self.choice_table = wx.Choice( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_tableChoices, 0 )
        self.choice_table.SetSelection( 0 )
        self.choice_table.Disable()
        bSizer2.Add( self.choice_table, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.OKBtn = wx.Button( self.panel, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.OKBtn, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.CancelBtn = wx.Button( self.panel, wx.ID_ANY, u"Cancel", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        bSizer2.Add( self.CancelBtn, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.panel.SetSizer( bSizer2 )
        self.panel.Layout()
        bSizer2.Fit( self.panel )
        bSizer1.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.Bind( wx.EVT_INIT_DIALOG, self.OnInit )
        self.choice_schema.Bind( wx.EVT_CHOICE, self.OnSchema )
        self.choice_table.Bind( wx.EVT_CHOICE, self.OnTable )
        
        # Buttons Events
        self.Bind(wx.EVT_BUTTON, self.OnOkBtn, self.OKBtn)
        self.Bind(wx.EVT_BUTTON, self.OnCancelBtn, self.CancelBtn)
        self.OKBtn.Enable(False)
        
        # Connect to db
        self.connection = connection
        
        # parent main
        self.main = parentMain
        
    
    def OnInit( self, event ):
        try:
            self.workdb = oracle.WorkDB(self.connection)
            schemas = self.workdb.get_schemas()
            self.choice_schema.SetItems(schemas)
            logging.info(u'list of schemas loaded successfully')
        except Exception, info:
            logging.error(u'list of schemas loading failed')
        
    def OnSchema( self, event ):
        try:
            self.schema = self.choice_schema.GetStringSelection()
            tables = self.workdb.get_tables(self.schema)
            self.choice_table.SetItems(tables)
            self.main.schema = self.schema
            self.choice_table.Enable()
            logging.info(u'list of tables loaded successfully')
            logging.info(u'schema %s choosed' % (self.schema))
        except Exception, info:
            logging.error(u'list of tables loading failed')

    def OnTable( self, event ):
        self.table = self.choice_table.GetStringSelection()
        self.main.table = self.table
        logging.info(u'table %s choosed' % (self.table))
        self.OKBtn.Enable(True)
        
    def OnOkBtn(self, event):
        self.main.DQ.Enable(4, True)
        self.main.DQ.Enable(5, True)
        self.main.regexp.Enable(6, True)
        self.main.regexp.Enable(7, True)
        self.main.logs.Enable(8, True)
        self.main.logs.Enable(9, True)
        self.Close()
        
    def OnCancelBtn(self, event):
        self.Destroy()
        
    def __del__( self ):
        pass