#-*- coding: utf8 -*-
import wx

class advices():
    def __init__(self, data):
        self.names = [u'Пустые значения', u'Не несущие информацию значения', u'Не соответствующие формату значения',
                                        u'Значение уровня шума', u'Идентифицируемость', u'Согласованность', u'Унификация', 
                                        u'Оперативность', u'Противоречивость', u'Степень классификации', 
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
        try:
            max_val = sum(self.data_req) / float(len(self.data_req))
        except ZeroDivisionError:
            wx.MessageBox(u'Вся статистика нулевая.')
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
        
        show = show_adv(self.ps, self.data_req, self.prev_dq)
        show.Show()

class show_adv ( wx.Frame ):
    
    def __init__( self, data, alldata, prev_dq ):
        wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Советы по оценке качества данных", pos = wx.DefaultPosition, size = wx.Size( 650,300 ), style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        main_sizer = wx.BoxSizer( wx.VERTICAL )
        
        self.params_adv_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.params_adv_splitter.Bind( wx.EVT_IDLE, self.params_adv_splitterOnIdle )
        self.params_adv_splitter.SetMinimumPaneSize( 123 )
        
        self.panel_params = wx.Panel( self.params_adv_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer_params = wx.BoxSizer( wx.VERTICAL )
        
        self.label_head_params = wx.StaticText( self.panel_params, wx.ID_ANY, u"Самые критичные параметры:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label_head_params.Wrap( -1 )
        sizer_params.Add( self.label_head_params, 0, wx.ALL, 5 )
                
        
        self.panel_params.SetSizer( sizer_params )
        self.panel_params.Layout()
        sizer_params.Fit( self.panel_params )
        self.panel_adv = wx.Panel( self.params_adv_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer_adv = wx.BoxSizer( wx.VERTICAL )
        
        self.html_page = self.CreateHTMLCtrl(self.panel_adv)
        sizer_adv.Add( self.html_page, 0, wx.ALL, 5 )
        
        
        self.panel_adv.SetSizer( sizer_adv )
        self.panel_adv.Layout()
        sizer_adv.Fit( self.panel_adv )
        self.params_adv_splitter.SplitVertically( self.panel_params, self.panel_adv, 267 )
        main_sizer.Add( self.params_adv_splitter, 1, wx.EXPAND, 5 )
        
        
        self.SetSizer( main_sizer )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        ### Function№1 ###
        perc = '%'
        for param in data:
            paramet = ('%s%s' % (param, perc))
            self.bad_params = wx.StaticText( self.panel_params, wx.ID_ANY, paramet, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
            self.bad_params.Wrap( -1 )
            sizer_params.Add( self.bad_params, 0, wx.ALL, 5 )
            
        ### Function№2 ###
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
            
            page = u'Если качество данных параметра - <b>%s%s</b> - увеличить на <u>10%s</u>, то качество данных возрастет на <u>%s%s</u> и итоговый процент будет составлять <u>%s%s</u>.<div><br /></div>' % (param, perc, perc, delta_dq, perc, future_dq, perc)
            
            self.html_page.AppendToPage(page)
        

        self.panel_adv.Bind(wx.EVT_LEFT_DCLICK, self.OnLEFT_DCLICK)
        self.panel_params.Bind(wx.EVT_LEFT_DCLICK, self.OnLEFT_DCLICK)

    def params_adv_splitterOnIdle( self, event ):
        self.params_adv_splitter.SetSashPosition( 208 )
        self.params_adv_splitter.Unbind( wx.EVT_IDLE )
            
    def __del__( self ):
        pass
    
    def OnLEFT_DCLICK(self, event):
        self.Close()
    
    def CreateHTMLCtrl(self, parent=None):
        if not parent:
            parent = self

        ctrl = wx.html.HtmlWindow(parent, -1, wx.DefaultPosition, wx.Size(400, 300))
        return ctrl
