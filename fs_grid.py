# coding=utf-8
import wx
import wx.grid
import logging
logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

###########################################################################
## Class fullgrid
###########################################################################

class fullgrid ( wx.Frame ):
    
    def __init__( self, gridtable ):
        wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1000,700 ))#, style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_grid2 = wx.grid.Grid( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, (950, 650), 0 )
        
        # Grid
        self.m_grid2.CreateGrid( 5, 5 )
        self.m_grid2.EnableEditing( True )
        self.m_grid2.EnableGridLines( True )
        self.m_grid2.EnableDragGridSize( False )
        self.m_grid2.SetMargins( 0, 0 )
        
        # Columns
        self.m_grid2.EnableDragColMove( False )
        self.m_grid2.EnableDragColSize( True )
        self.m_grid2.SetColLabelSize( 30 )
        self.m_grid2.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Rows
        self.m_grid2.EnableDragRowSize( True )
        self.m_grid2.SetRowLabelSize( 80 )
        self.m_grid2.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        
        # Cell Defaults
        self.m_grid2.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        bSizer2.Add( self.m_grid2, 0, wx.ALL, 5 )
        
        self.m_panel1.SetSizer( bSizer2 )
        self.m_panel1.Layout()
        bSizer2.Fit( self.m_panel1 )
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        self.m_grid2.SetTable(gridtable, True)
        self.m_grid2.AutoSizeColumns( True )
        
        self.m_panel1.Bind( wx.EVT_LEFT_DCLICK, self.OnRDC )
        #self.m_grid2.AutoSize(True)
    
    def OnRDC(self, event):
        self.Close()
        #self.Destroy()
    
    def __del__( self ):
        pass