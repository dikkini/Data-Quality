# -*- coding: utf8 -*-

import wx
import sys
import statistic
import wx.lib.mixins.listctrl as listmix #@UnusedImport
import adv
import oracle
import logging
import report_html

logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

class main_stat(listmix.ColumnSorterMixin): 
    def __init__( self, main, rows, ext_cols ): 
        self.main = main
        self.stat = statistic.stats(self.main.schema, self.main.table)
        
        self.ext_cols = ext_cols
        self.ext_cols.insert(0, u'Название параметра')
        
        data = []
        
        self.list = wx.ListCtrl(self.main.panelMainStat, 0,
                                 style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_EDIT_LABELS | wx.LC_SORT_ASCENDING | wx.LC_SINGLE_SEL)
        self.columns = self.main.main_stat_columns       
        for col, text in enumerate(self.columns):
            self.list.InsertColumn(col, text) 
        for item in rows:   
            info = '%s:(%s)' % (col, item)
            data.append(info)
            index = self.list.InsertStringItem(sys.maxint, item[0]) 
            for col, text in enumerate(item[1:]): 
                self.list.SetStringItem(index, col+1, text) 
                
        self.list.SetSize((900, 200))        
        self.list.SetColumnWidth(0, 120)   
        self.list.SetColumnWidth(1, 55) 
        self.list.SetColumnWidth(2, 55) 
        self.list.SetColumnWidth(3, 55)
        self.list.SetColumnWidth(4, 55)   
        self.list.SetColumnWidth(5, 55) 
        self.list.SetColumnWidth(6, 55) 
        self.list.SetColumnWidth(7, 55)
        self.list.SetColumnWidth(8, 55)   
        self.list.SetColumnWidth(9, 55) 
        self.list.SetColumnWidth(10, 55) 
        self.list.SetColumnWidth(11, 50)
        self.list.SetColumnWidth(12, 50)   
        self.list.SetColumnWidth(14, 50) 
        self.list.SetColumnWidth(15, 50) 
        self.list.SetColumnWidth(16, 40)
        self.list.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list)
        self.list.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.itemDataMap = data
        listmix.ColumnSorterMixin.__init__(self, 3)
        
        
        #self.ext_list.list.Show(False)
        
    def GetListCtrl(self):
        return self.list
    
    def getColumnText(self, index, col):
        item = self.list.GetItem(index, col)
        return item.GetText()
    
    def OnRightClick(self, event):
        index = self.list.GetFirstSelected()
        if index == -1:
            pass
        else:
            self.date = self.list.GetItemText(index)
            # make a menu
            menu = wx.Menu()
            # add some items
            menu.Append(1, u'Расширенную статистику')
            menu.Append(2, u'Советы по улучшению качества данных')
            menu.Append(3, u'Сформировать отчет')
            # binds menu events
            menu.Bind(wx.EVT_MENU, self.OnExtStat, id=1)
            menu.Bind(wx.EVT_MENU, self.OnAdviceMode, id=2)
            menu.Bind(wx.EVT_MENU, self.OnReport, id=3)
            self.list.PopupMenu(menu)
      
    def OnExtStat(self, event):
        try:
            self.ext_list.list.DeleteAllItems()
            self.ext_list.list.Destroy()
        except Exception:
            pass
        
#        self.main.Freeze()
        self.ext_stat = self.stat.take_ext_stat(self.date)
        self.ext_stat = [ i for i in self.ext_stat if i is not None] 
        self.ext_list = extend_stat(self.main.panelMainStat, self.ext_cols, self.ext_stat)
        self.main.sizer.Add(self.ext_list.list, 2, wx.EXPAND)
        self.main.panelMainStat.SetSizer(self.main.sbs)
        self.main.panelMainStat.Layout()
        size = self.main.GetSize()
        newsize = size - (1,1)
        print size
        print newsize
        self.main.SetSize(newsize)
        
        
        #Тут графический баг. При полноэкранном расширении получение расширенной статистики для результатов оценки качества данных идут с багом.
        
    def OnAdviceMode(self, event):
        mod = adv.advices(self.data)
        mod.TextAdv()
    
    def OnReport(self, event):
        report_html.make_report(self.columns, self.data, self.ext_cols, self.ext_stat, self.date)
        
    def OnColClick(self, event):
        print ("OnColClick: %d\n" % event.GetColumn())
        event.Skip()
    
    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        self.data = (self.getColumnText(self.currentItem, 1),
                            self.getColumnText(self.currentItem, 2),
                            self.getColumnText(self.currentItem, 3),
                            self.getColumnText(self.currentItem, 4),
                            self.getColumnText(self.currentItem, 5),
                            self.getColumnText(self.currentItem, 6),
                            self.getColumnText(self.currentItem, 7),
                            self.getColumnText(self.currentItem, 8),
                            self.getColumnText(self.currentItem, 9),
                            self.getColumnText(self.currentItem, 10),
                            self.getColumnText(self.currentItem, 11),
                            self.getColumnText(self.currentItem, 12),
                            self.getColumnText(self.currentItem, 13),
                            self.getColumnText(self.currentItem, 14))
        
        
class extend_stat(): 
    def __init__(self, panel, columns, rows): 
        
        self.list = wx.ListCtrl(panel, 0,
                                 style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_EDIT_LABELS | wx.LC_SORT_ASCENDING | wx.LC_SINGLE_SEL, 
                                 pos=(1,200))
        self.columns = columns          
        for col, text in enumerate(columns):
            self.list.InsertColumn(col, text) 
        for item in rows:   
            index = self.list.InsertStringItem(sys.maxint, item[0]) 
            for col, text in enumerate(item[1:]): 
                self.list.SetStringItem(index, col+1, text) 
        self.list.SetColumnWidth(0, 120)   
        self.list.SetColumnWidth(1, 55) 
        self.list.SetColumnWidth(2, 55) 
        self.list.SetColumnWidth(3, 55)
        self.list.SetColumnWidth(4, 55) 
        self.list.SetColumnWidth(5, 55)
        self.list.SetColumnWidth(6, 55) 
        self.list.SetColumnWidth(7, 55)
        self.list.SetColumnWidth(8, 55) 
        self.list.SetColumnWidth(9, 55)
        self.list.SetColumnWidth(10, 55) 
        self.list.SetColumnWidth(11, 55)
        self.list.SetColumnWidth(12, 55) 
        self.list.SetColumnWidth(13, 55)
        self.list.SetColumnWidth(14, 55) 
        self.list.SetColumnWidth(15, 55)
        self.list.SetColumnWidth(16, 40)
        self.list.SetSize((900,350))
        
class history_stat(): 
    def __init__(self, parent, columns, rows): 
        self.main = parent
        
        self.stat = statistic.stats(self.main.schema, self.main.table)
    
        self.list = wx.ListCtrl(self.main.panelHist, 0,
                                 style=wx.LC_REPORT
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 | wx.LC_SORT_ASCENDING
                                 | wx.LC_SINGLE_SEL, pos=(1,1)
                                 )
        self.columns = columns          
        for col, text in enumerate(columns):
            self.list.InsertColumn(col, text) 
        for item in rows:   
            index = self.list.InsertStringItem(sys.maxint, item[0]) 
            for col, text in enumerate(item[1:]): 
                self.list.SetStringItem(index, col+1, text) 
        self.list.SetColumnWidth(0, 120)   
        self.list.SetColumnWidth(1, 55) 
        self.list.SetColumnWidth(2, 55) 
        self.list.SetColumnWidth(3, 55)
        self.list.SetColumnWidth(4, 55) 
        self.list.SetColumnWidth(5, 55)
        self.list.SetColumnWidth(6, 55) 
        self.list.SetColumnWidth(7, 55)
        self.list.SetColumnWidth(8, 55) 
        self.list.SetColumnWidth(9, 55)
        self.list.SetColumnWidth(10, 55) 
        self.list.SetColumnWidth(11, 55)
        self.list.SetColumnWidth(12, 55) 
        self.list.SetColumnWidth(13, 55)
        self.list.SetColumnWidth(14, 55) 
        self.list.SetColumnWidth(15, 55)
        self.list.SetColumnWidth(16, 40)
        #self.list.SetSize((900,350))
        #self.list.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list)
        self.list.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
                
    def GetListCtrl(self):
        return self.list
    
    def getColumnText(self, index, col):
        item = self.list.GetItem(index, col)
        return item.GetText()
    
    def OnRightClick(self, event):
        index = self.list.GetFirstSelected()
        if index == -1:
            pass
        else:
            self.date = self.list.GetItemText(index)
            
            # make a menu
            menu = wx.Menu()
            
            # add some items
            menu.Append(1, u'Расширенную статистику')
            menu.Append(2, u'Советы по улучшению качества данных')
            menu.Append(3, u'Сформировать отчет')
            menu.Append(4, u'Удалить оценку')
            menu.Append(5, u'Обновить')

            # binds menu events
            menu.Bind(wx.EVT_MENU, self.OnExtStat, id=1)
            menu.Bind(wx.EVT_MENU, self.OnAdviceMode, id=2)
            menu.Bind(wx.EVT_MENU, self.OnReport, id=3)
            menu.Bind(wx.EVT_MENU, self.OnDelStat, id=4)
            menu.Bind(wx.EVT_MENU, self.OnRefresh, id=5)
            self.list.PopupMenu(menu)
    
    def OnExtStat(self, event):
        try:
            self.ext_cols = oracle.WorkDB(self.main.connection).get_cols(self.main.table)
            self.ext_cols.insert(0, u'Название параметра')
            self.ext_stat = self.stat.take_ext_stat(self.date)
            self.ext_stat = [ i for i in self.ext_stat if i is not None] 
            frame = Popup(self.ext_cols, self.ext_stat)
            frame.Show()
        except Exception, info:
            print info
            if 'object is not subscriptable' in str(info):
                wx.MessageBox(u'Для данной статистике нет расширенной статистики')

    def OnAdviceMode(self, event):
        mod = adv.advices(self.data)
        mod.TextAdv()
    
    def OnReport(self, event):
        ext_cols = oracle.WorkDB(self.main.connection).get_cols(self.main.table)
        ext_cols.insert(0, u'Название параметра')
        ext_stat = self.stat.take_ext_stat(self.date)
        report_html.make_report(self.columns, self.data, ext_cols, ext_stat, self.date)

    def OnDelStat(self, event):
        self.stat.del_stat(self.date)
        self.main.RefrshHist()
        #self.list.DeleteAllItems()
        #self.stat.history_stat(self.main)

    def OnColClick(self, event):
        print ("OnColClick: %d\n" % event.GetColumn())
        event.Skip()
    
    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        self.data = (self.getColumnText(self.currentItem, 1),
                            self.getColumnText(self.currentItem, 2),
                            self.getColumnText(self.currentItem, 3),
                            self.getColumnText(self.currentItem, 4),
                            self.getColumnText(self.currentItem, 5),
                            self.getColumnText(self.currentItem, 6),
                            self.getColumnText(self.currentItem, 7),
                            self.getColumnText(self.currentItem, 8),
                            self.getColumnText(self.currentItem, 9),
                            self.getColumnText(self.currentItem, 10),
                            self.getColumnText(self.currentItem, 11),
                            self.getColumnText(self.currentItem, 12),
                            self.getColumnText(self.currentItem, 13),
                            self.getColumnText(self.currentItem, 14))
    def OnRefresh(self, event):
#        self.list.DeleteAllItems()
#        self.stat.history_stat(self.main)
        self.main.RefrshHist()
        
    def destr(self):
        self.list.Destroy()

class Popup ( wx.Frame ):
    
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
        
        
        self.SetSizer( bSizer10 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        self.list.Bind( wx.EVT_LEFT_DCLICK, self.OnELD )

    def OnELD(self, event):
        self.Destroy()