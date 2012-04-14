# -*- coding: utf-8 -*- 
import wx
import sys

class MainWindow ( wx.Frame ):
    
    def __init__( self, columns, rows ):
        wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 900,250 ), style = wx.CAPTION|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.Size( 700,230 ), wx.Size( 900,250 ) )
        
        bSizer10 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel5 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer11 = wx.BoxSizer( wx.VERTICAL )
        
        self.list = wx.ListCtrl(self.m_panel5, 0,
                                 style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_EDIT_LABELS | wx.LC_SORT_ASCENDING | wx.LC_SINGLE_SEL, 
                                 pos=(1,1))
        self.columns = columns  
        self.columns.pop(0)
        self.columns.insert(0, u'Название параметра')        
        for col, text in enumerate(columns):
            self.list.InsertColumn(col, text) 
        for item in rows:   
            index = self.list.InsertStringItem(sys.maxint, item[0]) 
            for col, text in enumerate(item[1:]): 
                self.list.SetStringItem(index, col+1, text) 
        self.list.SetColumnWidth(0, 120)   
        self.list.SetColumnWidth(1, 45) 
        self.list.SetColumnWidth(2, 45) 
        self.list.SetColumnWidth(3, 45)
        self.list.SetColumnWidth(4, 45) 
        self.list.SetColumnWidth(5, 45)
        self.list.SetColumnWidth(6, 45) 
        self.list.SetColumnWidth(7, 45)
        self.list.SetColumnWidth(8, 45) 
        self.list.SetColumnWidth(9, 45)
        self.list.SetColumnWidth(10, 45) 
        self.list.SetColumnWidth(11, 45)
        self.list.SetColumnWidth(12, 45) 
        self.list.SetColumnWidth(13, 45)
        self.list.SetColumnWidth(14, 45) 
        self.list.SetColumnWidth(15, 45)
        self.list.SetColumnWidth(16, 40)
        self.list.SetSize((900,350))
        
     
        self.m_panel5.SetSizer( bSizer11 )
        self.m_panel5.Layout()
        bSizer11.Fit( self.m_panel5 )
        bSizer10.Add( self.m_panel5, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.combobox = wx.ComboBox(self.list, -1, choices=["That", "Was", "A", "Nice", "Holiday!"], style=wx.CB_READONLY|wx.CB_DROPDOWN)
        
        self.SetSizer( bSizer10 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnELD)
        self.list.Bind(wx.EVT_RIGHT_DCLICK, self.OnRDC)

    def OnELD(self, event):
        self.Destroy()
        
    def OnRDC(self, event):
        last = self.list.Append(self.combobox)
cols = ['test0', 'test1', 'test2', 'test3', 'test4']
rows = [['123', '456', '789', '012', '345']]

cols1 = ['test5', 'test6', 'test7', 'test8', 'test9']
rows1 = [['543', 'asdasd', 'asfw23asf', '7892dasf', 'asf23']]
        
        
        
class A(wx.App):
    def __init__(self, *a, **k):
        wx.App.__init__(self, *a, **k)
        frame = MainWindow(cols, rows)
        frame.Show()
        self.SetTopWindow(frame)

if __name__ == '__main__':
    a = A(
        redirect=False,
        filename=None,
        useBestVisual=True)
    a.MainLoop()