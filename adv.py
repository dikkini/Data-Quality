#-*- coding: utf8 -*-
import wx

class advices():
    def __init__(self, data):
        self.names = [u'Пустые значения', u'Не несущие информацию значения', u'Не соответствующие формату значения',
                                        u'Значение уровня шума', u'Идентифицируемость', u'Согласованность', u'Унификация', 
                                        u'Оперативность', u'Противоречивость', u'Достоверность', u'Степень классификации', 
                                        u'Степень структуризации']
        data = list(data)
        data.pop()
        self.prev_dq = data[-1]
        data.pop()
        self.data = map(lambda a: float(a) if a != '-' else 0, data)
#        self.minperc = min(self.data)
#        self.count = len(self.data)
#        self.param12 = 'working!'
        
# ----- функция получения списка минимальных значений оценки ---- 
    def get_mins(self):
        # получение среднего. удаление неиспользуемых параметров
        # убираем одинаковые значения -- useless (???)
        self.data_req = list(set(self.data))
        for i in self.data_req:
            if not i:
                self.data_req.remove(i)
        max_val = sum(self.data_req) / float(len(self.data_req))
        #minimals = ((idx, i) for idx, i in enumerate(self.data) if i < max_val)
        minimals = ((idx, i) for idx, i in enumerate(self.data) if i < max_val and isinstance(i, float))
        return sorted(minimals, key=lambda a: a[1])
        
    def TextAdv(self):
        data = self.get_mins()
        self.ps = []
        for num_param in data:
            num = num_param[0]
            perc = num_param[1]
            if num == 0:
                self.param0 = (u'%s: %s' % (self.names[0], perc))
                self.ps.append(self.param0)
            if num == 1:
                self.param1 = (u'%s: %s' % (self.names[1], perc))
                self.ps.append(self.param1)
            if num == 2:
                self.param2 = (u'%s: %s' % (self.names[2], perc))
                self.ps.append(self.param2)
            if num == 3:
                self.param3 = (u'%s: %s' % (self.names[3], perc))
                self.ps.append(self.param3)
            if num == 4:
                self.param4 = (u'%s: %s' % (self.names[4], perc))
                self.ps.append(self.param4)
            if num == 5:
                self.param5 = (u'%s: %s' % (self.names[5], perc))
                self.ps.append(self.param5)
            if num == 6:
                self.param6 = (u'%s: %s' % (self.names[6], perc))
                self.ps.append(self.param6)
            if num == 7:
                self.param7 = (u'%s: %s' % (self.names[7], perc))
                self.ps.append(self.param7)
            if num == 8:
                self.param8 = (u'%s: %s' % (self.names[8], perc))
                self.ps.append(self.param8)
            if num == 9:
                self.param9 = (u'%s: %s' % (self.names[9], perc))
                self.ps.append(self.param9)
            if num == 10:
                self.param10 = (u'%s: %s' % (self.names[10], perc))
                self.ps.append(self.param10)
            if num == 11:
                self.param11 = (u'%s: %s' % (self.names[11], perc))
                self.ps.append(self.param11)
        
        show = ShowAdv(self.ps, self.data_req, self.prev_dq)
        show.Show()
            
class ShowAdv ( wx.Frame ):
    def __init__( self, data, alldata, prev_dq ):
        wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Data Quality -- Советы", pos = wx.DefaultPosition, size = wx.Size( 700,400 ), style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
        
        self.m_panel2 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer6 = wx.BoxSizer( wx.VERTICAL )
        perc = '%'
        for param in data:
            paramet = ('%s%s' % (param, perc))
            self.bad_params = wx.StaticText( self.m_panel2, wx.ID_ANY, paramet, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
            self.bad_params.Wrap( -1 )
            bSizer6.Add( self.bad_params, 0, wx.ALL, 5 )
        
        self.m_panel2.SetSizer( bSizer6 )
        self.m_panel2.Layout()
        bSizer6.Fit( self.m_panel2 )
        self.m_panel3 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer7 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_panel3.SetSizer( bSizer7 )
        self.m_panel3.Layout()
        bSizer7.Fit( self.m_panel3 )
        self.m_splitter1.SplitHorizontally( self.m_panel2, self.m_panel3, 0 )
        bSizer1.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        ### Function ###
        for param in data:
            temp = param
            parse = temp.split(':')
            if len(parse) > 1:
                temp = parse[-1]
                temp = temp.strip()
                try:
                    number = float(temp)
                except ValueError:
                    wx.MessageBox(u'ошибка')
            alldata.remove(number)
            future_element = number + 10
            alldata.append(future_element)
            future_dq = sum(alldata) / len(alldata)
            delta_dq = round(float(future_dq), 2) - round(float(prev_dq), 2)
            future_dq = round(future_dq, 2)
            
            info = (u'Если качество данных параметра -  %s%s - увеличить на 10%s,\n то качество данных возрастет на %s%s и итоговый процент будет составлять %s%s.                       ' % (param, perc, perc, delta_dq, perc, future_dq, perc))
            print info
            self.text_adv = wx.StaticText( self.m_panel3, wx.ID_ANY, info, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
            #self.text_adv.Wrap( -1 )
            bSizer3.Add( self.text_adv, 0, wx.ALL, 5 )
        
        
        self.m_panel2.Bind(wx.EVT_LEFT_DCLICK, self.OnLEFT_DCLICK)
    
    def OnLEFT_DCLICK(self, event):
        self.Close()

    def m_splitter1OnIdle( self, event ):
        self.m_splitter1.SetSashPosition( 0 )
        self.m_splitter1.Unbind( wx.EVT_IDLE )