import wx
import re, os, sys
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)

class QueueDialog(wx.Dialog):

    def __init__(self, parent, title):
        super(QueueDialog, self).__init__(parent=parent, 
            title=title, size=(400, 500))


        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(panel, label='Queue')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)

        hbox3 = wx.BoxSizer(wx.VERTICAL)
        listB = CheckListCtrl(panel)
        listB.InsertColumn(0, "Test", width=100)
        listB.InsertColumn(1, "Status", wx.LIST_FORMAT_RIGHT)
        hbox3.Add(listB, 1, wx.EXPAND)

        dalist = ["heh", "ha", "hello"]
        for name in dalist[0:3]:
            index = listB.InsertStringItem(sys.maxint, name[0:-1])

        sbs.Add(hbox3, proportion=1,flag=wx.EXPAND|wx.ALL)
        panel.SetSizer(sbs)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        okButton = wx.Button(self, label='OK')
        closeButton = wx.Button(self, label='Cancel')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(panel, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        vbox.Add(hbox2, flag= wx.ALIGN_CENTER|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

    def OnClose(self, e):
        self.Destroy()


class window(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(600, 400))

        e = QueueDialog(None, title='Queue')
        e.ShowModal()
        e.Destroy()

        self.Centre()
        self.Show(True)

app = wx.App(0)
window(None, -1, 'e')
app.MainLoop()