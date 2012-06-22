# -*- coding: utf-8 -*- 
import wx

class advices():
    def __init__(self, data):
        self.names = [u'Пустые значения', u'Не несущие информацию значения', u'Не соответствующие формату значения',
                                        u'Значение уровня шума', u'Идентифицируемость', u'Согласованность', u'Унификация', 
                                        u'Оперативность', u'Противоречивость', u'Степень классификации', 
                                        u'Степень структуризации']
        self.data_normal = data
        print 'FULLLLLL DATA', data
        data = list(data)
        data.pop()
        print 'fulldata-1', data
        self.prev_dq = self.max_val = data.pop()
        print 'max_val and prev_dq:', self.max_val
        self.data = data
        
    def get_future_dq(self, data):
        data = map(lambda a: float(a) if a != '-' else 111, data)
        
        data[0] = float(100 - float(data[0]))
        data[1] = float(100 - float(data[1]))
        data[2] = float(100 - float(data[2]))
        data[3] = float(100 - float(data[3]))
        data[8] = float(100 - float(data[8]))
        print 'future data 1:', data
        if data[0] == -11:
            data[0] = 0
        if data[1] == -11:
            data[1] = 0
        if data[2] == -11:
            data[2] = 0
        if data[3] == -11:
            data[3] = 0
        if data[4] == 111:
            data[4] = 0
        if data[5] == 111:
            data[5] = 0
        if data[6] == 111:
            data[6] = 0
        if data[7] == 111:
            data[7] = 0
        if data[8] == -11:
            data[8] = 0
        if data[9] == 111:
            data[9] = 0
        if data[10] == 111:
            data[10] = 0
        print 'fut data 2:', data
        dq = sum(data)
        return dq
    
    def get_advices(self, flag):
        perc = '%'
        pages = []
        params = []
        if self.data[0] == '-' or self.data[0] < self.max_val:
            pass
        if self.data[0] != '-' and self.data[0] > self.max_val and (float(self.data[0])+10 < 100) and (float(self.data[0])-10 > 0):
            index = 0
            name_param = self.names[0]
            pages.append(self.take_negative_page(name_param, index, self.data))
            params.append(u'%s: %s%s' % (self.names[0], self.data_normal[0], perc))
            
        if self.data[1] == '-' or self.data[1] < self.max_val:
            pass
        if self.data[1] != '-' and self.data[1] > self.max_val and (float(self.data[1])+10 < 100) and (float(self.data[1])-10 > 0):
            index = 1
            name_param = self.names[1]
            pages.append(self.take_negative_page(name_param, index, self.data))
            params.append(u'%s: %s%s' % (self.names[1], self.data_normal[1], perc))
        
        if self.data[2] == '-' or self.data[2] < self.max_val:
            pass
        if self.data[2] != '-' and self.data[2] > self.max_val and (float(self.data[2])+10 < 100) and (float(self.data[2])-10 > 0):
            index = 2
            name_param = self.names[2]
            pages.append(self.take_negative_page(name_param, index, self.data))
            params.append(u'%s: %s%s' % (self.names[2], self.data_normal[2], perc))
        
        if self.data[3] == '-' or self.data[3] < self.max_val:
            pass
        if self.data[3] != '-' and self.data[3] > self.max_val and (float(self.data[3])+10 < 100) and (float(self.data[3])-10 > 0):
            index = 3
            name_param = self.names[3]
            pages.append(self.take_negative_page(name_param, index, self.data))
            params.append(u'%s: %s%s' % (self.names[3], self.data_normal[3], perc))
        
        if self.data[4] == '-' or self.data[4] > self.max_val:
            pass
        if self.data[4] != '-' and self.data[4] < self.max_val and (float(self.data[4])+10 < 100):
            index = 4
            name_param = self.names[4]
            pages.append(self.take_negative_page(name_param, index, self.data))
            params.append(u'%s: %s%s' % (self.names[4], self.data_normal[4], perc))
        
        if self.data[5] == '-' or self.data[5] > self.max_val:
            pass
        if self.data[5] != '-' and self.data[5] < self.max_val and (float(self.data[5])+10 < 100):
            index = 5
            name_param = self.names[5]
            pages.append(self.take_negative_page(name_param, index, self.data))
            params.append(u'%s: %s%s' % (self.names[5], self.data_normal[5], perc))
        
        if self.data[6] == '-' or self.data[6] > self.max_val:
            pass
        if self.data[6] != '-' and self.data[6] < self.max_val and (float(self.data[6])+10 < 100):
            index = 6
            name_param = self.names[6]
            pages.append(self.take_negative_page(name_param, index, self.data))
            params.append(u'%s: %s%s' % (self.names[6], self.data_normal[6], perc))
        
        if self.data[7] == '-' or self.data[7] > self.max_val:
            pass
        if self.data[7] != '-' and self.data[7] < self.max_val and (float(self.data[7])+10 < 100):
            index = 7
            name_param = self.names[7]
            pages.append(self.take_negative_page(name_param, index, self.data))
            params.append(u'%s: %s%s' % (self.names[7], self.data_normal[7], perc))
        
        if self.data[8] == '-' or self.data[8] < self.max_val:
            pass
        if self.data[8] != '-' and self.data[8] > self.max_val and (float(self.data[8])+10 < 100) and (float(self.data[8])-10 > 0):
            index = 8
            name_param = self.names[8]
            pages.append(self.take_negative_page(name_param, index, self.data))
            params.append(u'%s: %s%s' % (self.names[8], self.data_normal[8], perc))
        
        if self.data[9] == '-' or self.data[9] > self.max_val:
            pass
        if self.data[9] != '-' and self.data[9] < self.max_val and (float(self.data[9])+10 < 100):
            index = 9
            name_param = self.names[9]
            pages.append(self.take_negative_page(name_param, index, self.data))
            params.append(u'%s: %s%s' % (self.names[9], self.data_normal[9], perc))
        
        if self.data[10] == '-' or self.data[10] > self.max_val:
            pass
        if self.data[10] != '-' and self.data[10] < self.max_val and (float(self.data[10])+10 < 100):
            index = 10
            name_param = self.names[10]
            pages.append(self.take_negative_page(name_param, index, self.data))
            params.append(u'%s: %s%s' % (self.names[10], self.data_normal[10], perc))
        
        advices = [params, pages]
        if flag is True:
            show = show_adv( params, pages )
            show.Show()
        else:
            return advices
    
    def take_negative_page(self, name_param, index, data):
        perc = '%'
        dat = []
        if index == 0 or index == 1 or index == 2 or index == 3 or index == 8:
            new_value = float(data[index]) - 10
        if index == 4 or index == 5 or index == 6 or index == 7 or index == 9 or index == 10:
            new_value = float(data[index]) + 10
        data[index] = new_value
        for i in data:
            if i == '-':
                pass
            else:
                dat.append(float(i))
        future_dq = self.get_future_dq(data) / len(dat)
        future_dq = float(future_dq)
        future_dq = round(future_dq, 2)
        delta = future_dq - round(float(self.prev_dq), 2)
        if index == 0 or index == 1 or index == 2 or index == 3 or index == 8:
            text = (u'Если качество данных - <b>%s</b> - уменьшить на <u>10%s</u>, то есть количество записей параметра <b>%s</b> уменьшится на <u>10%s</u>, \
                то качество данных возрастет на <u>%s%s</u> и \
                итоговый процент будет составлять <u>%s%s</u>.<div><br /></div>' % (name_param, perc, name_param, perc, delta, perc, future_dq, perc))
        if index == 4 or index == 5 or index == 6 or index == 7 or index == 9 or index == 10:
            text = (u'Если качество данных - <b>%s</b> - увеличить на <u>10%s</u>, то есть количество записей параметра <b>%s</b> увеличится на <u>10%s</u>, \
                то качество данных возрастет на <u>%s%s</u> и \
                итоговый процент будет составлять <u>%s%s</u>.<div><br /></div>' % (name_param, perc, name_param, perc, delta, perc, future_dq, perc))
        return text


class show_adv ( wx.Frame ):
    
    def __init__( self, adv_params, pages ):
        wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Советы по оценке качества данных", pos = wx.DefaultPosition, size = wx.Size( 650,300 ), style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        main_sizer = wx.BoxSizer( wx.VERTICAL )
        
        self.params_adv_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.params_adv_splitter.Bind( wx.EVT_IDLE, self.params_adv_splitterOnIdle )
        self.params_adv_splitter.SetMinimumPaneSize( 123 )
        
        self.panel_params = wx.Panel( self.params_adv_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer_params = wx.BoxSizer( wx.VERTICAL )
        
        self.label_head_params = wx.StaticText( self.panel_params, wx.ID_ANY, u"Критичные параметры:", wx.DefaultPosition, wx.DefaultSize, 0 )
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
        for param in adv_params:
            self.bad_params = wx.StaticText( self.panel_params, wx.ID_ANY, param, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
            self.bad_params.Wrap( -1 )
            sizer_params.Add( self.bad_params, 0, wx.ALL, 5 )
            
        ### Function№2 ###
        for page in pages:
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
