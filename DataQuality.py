# -*- coding: utf8 -*-

import wx
import wx.aui
import schematable
import connections_manager
import os
import calculation
import results
import statistic
import help
import about
import logging
import os
import sys
import regexps_editor
import params_chooser

try:
    from agw import pybusyinfo as PBI
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.pybusyinfo as PBI
    
logging.basicConfig(filename='journal_events.log',format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)

# Set Envroiment
# Encoding for database Oracle
os.environ["NLS_LANG"] = "RUSSIAN_CIS.CL8MSWIN1251"
os.putenv("ORACLE_HOME","/usr/lib/oracle/11.2/client")

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):
    
    def __init__( self ):
        wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Data Quality -- Главное окно", 
                            pos = wx.DefaultPosition, size = wx.Size( 900,600 ) )
        
        self.SetSizeHintsSz( wx.Size( 1000,600 ), wx.DefaultSize )
        
        self.sizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.notebook = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_DEFAULT_STYLE )
        self.panel1 = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sizer2 = wx.BoxSizer( wx.VERTICAL )

        self.panel1.SetSizer( sizer2 )
        self.panel1.Layout()
        sizer2.Fit( self.panel1 )
        html_start_panel = self.CreateHTMLCtrl(self.panel1)
        self.notebook.AddPage(html_start_panel , u"Добро пожаловать", True, wx.NullBitmap )
        
        start_page = '<h4><img src="./data/img/mephi_logo.png" border="0" />&nbsp;Data Quality -- &nbsp;приложение для оценки качества данных.</h4>' \
                     '<div>Данная страничка расскажет о базовых элементах программы и поможет начать работу. Больше информации по работе с программой Вы можете найти в "Справке" (вызвать которую можно нажав клавишу F1) в разделе меню-бара "Помощь".</div>' \
                     '<div><br /></div>' \
                     '<div>Наверху окна можно увидеть главное навигационное меню. Основные функции находятся в пунктах меню, в различных разделах. Внизу окна программы статусная строка, объясняющая каждый пункт меню.</div>' \
                     '<div><br /></div>' \
                     '<div>Для начала работы необходимо:</div>' \
                     '<div><br /></div> <div> <ul>' \
                     '<li>Подключиться к базе данных Oracle</li>' \
                     '<li>Выбрать схему и таблицу</li></ul>' \
                     '<div>Далее уже можно приступать к непосредственному процессу оценки качества данных. Начать необходимо с написания регулярных выражений в модуле "Отладка регулярных выражений" находящемся в разделе меню-бара "Регулярные выражения".</div></div>' \
                     '<div><br /></div>' \
                     '<div>Удачи в работе!</div>' \
                     '<div><br /></div>' \
        
        html_start_panel.SetPage(start_page)
        
        self.sizer3 = wx.BoxSizer( wx.VERTICAL )
        
        self.sizer1.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 5 )
        
        self.SetSizer( self.sizer1 )
        self.Layout()
        self.menubar = wx.MenuBar( 0 )
        self.BD = wx.Menu()
        self.m_menuItem1 = wx.MenuItem( self.BD, 1, u"Подключиться к базе\tCtrl+F", u'Выполнить подключение к базе данных', wx.ITEM_NORMAL )
        self.BD.AppendItem(self.m_menuItem1, )
        
        self.m_menuItem2 = wx.MenuItem( self.BD, 2, u"Выбрать таблицу\tCtrl+T", u'Выбрать схему и таблицу для оценки качества данных', wx.ITEM_NORMAL )
        self.BD.AppendItem( self.m_menuItem2 )
        
        self.m_menuItem3 = wx.MenuItem( self.BD, 3, u"Отключиться и выйти\tCtrl+Q", 
                                        u'Отключиться от базы данных в выйти из приложения', wx.ITEM_NORMAL )
        
        self.BD.AppendItem( self.m_menuItem3 )
        
        self.menubar.Append(self.BD, u"База данных")
        
        self.DQ = wx.Menu()
        self.m_menuItem4 = wx.MenuItem( self.DQ, 4, u"Выполнить оценку качества данных\tCtrl+D", 
                                        u'Произвести запуск процесса оценки качества данных', wx.ITEM_NORMAL )
        
        self.DQ.AppendItem( self.m_menuItem4 )
        
        self.m_menuItem5 = wx.MenuItem( self.DQ, 5, u"Посмотреть историю оценок\tCtrl+H", 
                                        u'Просмотр истории оценок выбранной таблицы.', wx.ITEM_NORMAL )
        
        self.DQ.AppendItem( self.m_menuItem5 )
        
        self.menubar.Append( self.DQ, u"Оценка" ) 
        
        self.regexp = wx.Menu()
        self.m_menuItem6 = wx.MenuItem( self.regexp, 6, u"Отладка регулярных выражений\tCtrl+R", 
                                        u'Запуск инструмента для отладки регулярных выражений.', wx.ITEM_NORMAL )
        
        self.regexp.AppendItem( self.m_menuItem6 )
        
        self.m_menuItem7 = wx.MenuItem( self.regexp, 7, u"Выбор регулярных выражения для оценки\tCtrl+E", 
                                        u'На основе выбранных параметрах будет производиться оценка качества данных', wx.ITEM_NORMAL )
        
        self.regexp.AppendItem( self.m_menuItem7 )
        
        self.menubar.Append( self.regexp, u"Регулярные выражения" ) 
        
        self.logs = wx.Menu()
        self.m_menuItem8 = wx.MenuItem( self.logs, 8, u"Журнал событий\tCtrl+I", wx.EmptyString, wx.ITEM_NORMAL )
        self.logs.AppendItem( self.m_menuItem8 )
        
        self.menubar.Append( self.logs, u"Журналы" ) 
        
        self.help = wx.Menu()
        self.m_menuItem10 = wx.MenuItem( self.help, 10, u'О программе\tF2', wx.EmptyString, wx.ITEM_NORMAL)
        self.help.AppendItem( self.m_menuItem10 )
        
        self.m_menuItem11 = wx.MenuItem( self.help, 11, u'Справка\tF1', u'Вызов справки по приложению', wx.ITEM_NORMAL)
        self.help.AppendItem( self.m_menuItem11 )
        
        self.menubar.Append( self.help, u'Помощь')
        self.SetMenuBar( self.menubar )
        
        self.statusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
        
        self.Centre( wx.BOTH )
        
        #Connection vars
        self.schema = None
        self.connection = None
        self.table = None
        self.schema = None
        
        #DQ vars
        self.weights = None
        self.using_params = None
        self.user_choice_catalog = None
        self.user_number_allfields = None
        self.user_number_composite_fileds = None

        #Disable menuitems
        self.BD.Enable(2, False)
        self.DQ.Enable(4, False)
        self.DQ.Enable(5, False)
        self.regexp.Enable(6, False)
        self.regexp.Enable(7, False)
        self.logs.Enable(8, False)
        
        #Binds on MenuItems
        self.Bind(wx.EVT_MENU, self.ConnectDB, id=1)
        self.Bind(wx.EVT_MENU, self.ChooseTable, id=2)
        self.Bind(wx.EVT_MENU, self.DisconnectDB, id=3)
        self.Bind(wx.EVT_MENU, self.DoDQ, id=4)
        self.Bind(wx.EVT_MENU, self.HistDQ, id=5)
        self.Bind(wx.EVT_MENU, self.EditRegexps, id=6)
        self.Bind(wx.EVT_MENU, self.ChooseParams, id=7)
        self.Bind(wx.EVT_MENU, self.logEvents, id=8)
        self.Bind(wx.EVT_MENU, self.About, id=10)
        self.Bind(wx.EVT_MENU, self.show_help, id=11)
        
        #Notebook events
        self.notebook.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnTabClose)
        
        # Statusbar Text
        self.statusbar.SetStatusText(u'Это статусная строка, здесь будет информацию о текущем состоянии программы, а также подсказки по ходу работы с программой.')
        
        # Main results data
        self.main_stat_columns = [u'Дата', u'Пустые', u'Не несущие информацию', u'Не соответствующие формату', u'Уровень шума', 
                          u'Идентифицируемость', u'Согласованность', u'Унификация', u'Оперативность', 
                          u'Противоречивость', u'Степень классификации', u'Степень структуризации', u'Степень идентифицируемости', u'Итого', u'Таблица'] 
        
        logging.info(u'######################################################################################')
        logging.info(u'start session')
    
    def CreateHTMLCtrl(self, parent=None):
        if not parent:
            parent = self

        ctrl = wx.html.HtmlWindow(parent, -1, wx.DefaultPosition, wx.Size(400, 300))
        return ctrl    
        
    def ConnectDB(self, event):
        logging.info(u'connect to db')
        frame = connections_manager.connections(self)
        frame.Show()
        self.statusbar.SetStatusText(u'Выполняется подключение к базе')
        self.flagres = None

        
    def ChooseTable(self, event):
        self.using_params = None
        logging.info(u'choose table')
        frame = schematable.choose_table(self.connection, self)
        frame.ShowModal()
        
    def DisconnectDB(self, event):
        try:
            self.connection.close()
            self.Destroy()
            sys.exit()
            logging.info(u'end session: %s')
        except Exception, info:
            if "'NoneType' object has no attribute 'close'" in info:
                logging.info(u'end session. but there are no connection to db')
            self.Destroy()
            logging.error(u'end session error - code 214: %s' % str(info))
            sys.exit()
    
    def DoDQ(self, event):
        message = 'Пожалуйста подождите, происходит оценка качества данных...'
        try:
            if not self.using_params or sum(self.using_params) == 0:
                wx.MessageBox(u'Вы не выбрали ни одного параметра для оценки!')
                logging.error(u'failed calculation dq - code 222: NO PARAMS FOR DATA QUALITY')
                return False
            if self.flagres is None:
                busy = PBI.PyBusyInfo(message, parent=None, title="Оцениваем данные...")
                wx.Yield()
                
                self.panelMainStat = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
                self.dataquality = calculation.DQ(self.connection)
                print self.user_number_allfields
                print self.user_number_composite_fileds
                self.flagres = result = self.dataquality.mathDQ(self.weights, self.using_params, self.user_choice_catalog, self.user_number_allfields, self.user_number_composite_fileds, self.schema,  self.table)
                if result is None:
                    event.Skip()
                    return None
                self.notebook.AddPage( self.panelMainStat, u"Результаты оценки качества данных", False, wx.NullBitmap )
                self.result_ctrl = results.main_stat( self, result, self.dataquality.namecols )
                
                self.sb = wx.StaticBox(self.panelMainStat)
                self.sbs = wx.StaticBoxSizer(self.sb, orient=wx.VERTICAL)
                self.sizer = wx.BoxSizer(wx.VERTICAL)
            
                self.sizer.Add(self.result_ctrl.list, 1, wx.EXPAND)
                self.sbs.Add(self.sizer, proportion=1,flag=wx.EXPAND|wx.ALL)
                self.panelMainStat.SetSizer(self.sbs)
                self.panelMainStat.Layout()
            
                del busy
            else:
                busy = PBI.PyBusyInfo(message, parent=None, title="Оцениваем данные...")
                wx.Yield()
                    
                result2 = self.dataquality.mathDQ(self.weights, self.using_params, self.user_choice_catalog, self.user_number_allfields, self.user_number_composite_fileds, self.schema,  self.table)
                self.result_ctrl.list.Append(result2[0])
                
                self.panelMainStat.SetSizer(self.sbs)
                self.panelMainStat.Layout()
                
                del busy
        except Exception, info:
                wx.MessageBox(str(info))
                logging.error(u'starting calculate dq process failed - code 260: %s' % (str(info)))
    
    def OnTabClose(self, event):
        temp_page = event.GetSelection()
        sel_page = self.notebook.GetPageText(temp_page)
        if u'Результаты оценки качества данных' in sel_page:
            self.flagres = None
        
    def HistDQ(self, event):
        try:
            logging.info(u'open local history')
            self.panelHist = wx.Panel( self.notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
            hist_title = (u"История оценки качества данных %s.%s" % (self.schema, self.table))
            self.notebook.AddPage( self.panelHist, hist_title, False, wx.NullBitmap )
            self.histcols = self.main_stat_columns
            histrows = statistic.stats(self.schema, self.table).history_stat(self) 
            self.histres = results.history_stat(self, self.histcols, histrows, self.schema, self.table)
            
            sb = wx.StaticBox(self.panelHist)
            sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
            sizer = wx.BoxSizer(wx.VERTICAL)
            
            sizer.Add(self.histres.list, 1, wx.EXPAND)
            sbs.Add(sizer, proportion=1,flag=wx.EXPAND|wx.ALL)
            self.panelHist.SetSizer(sbs)
            self.panelHist.Layout()
            
        except TypeError, info:
            wx.MessageBox(str(info))
            logging.error(u'error while looking history - code: 289 - %s' % str(info))
    
    def RefrshHist(self):
        self.histres.destr()
        histrows = statistic.stats(self.schema, self.table).history_stat(self) 
        self.histres = results.history_stat(self, self.histcols, histrows, self.schema, self.table)
            
        sb = wx.StaticBox(self.panelHist)
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
            
        sizer.Add(self.histres.list, 1, wx.EXPAND)
        sbs.Add(sizer, proportion=1,flag=wx.EXPAND|wx.ALL)
        self.panelHist.SetSizer(sbs)
        self.panelHist.Layout()
        
    def EditRegexps(self, event):
        if self.connection is None:
            wx.MessageBox(u'Подключитесь к базе!')
            if self.table is None:
                wx.MessageBox(u'Выберите таблицу!')
        else:
            logging.info(u'launch edit regexps module')
            regexps_editor.page_editor(self, self.schema, self.table, self.connection)
            
            current_size = self.GetSize()
            new_size = current_size + (1,1)
            self.SetSize(new_size)
            
            if self.IsMaximized():
                self.SetFocus()
        
    def ChooseParams(self, event):
        try:
            params_chooser.frame_chooser(self, self.schema, self.table, self.connection).Show()
        except Exception, info:
            wx.MessageBox(info)
        
    def logEvents(self, event):
        try:
            file = 'journal_events.log'
            os.system('notepad.exe ' + file)
        except Exception, info:
            logging.error(u'error while opening journal events - code 333 ', str(info))
        
    def About(self, event):
        frame = about.about()
        frame.Show()
    
    def show_help(self, event):
        frame = help.help_frame()
        frame.Show()
        
        
    def __del__( self ):
        pass



class A(wx.App):
    def __init__(self, *a, **k):
        wx.App.__init__(self, *a, **k)
        frame = MainWindow()
        frame.Show()
        self.SetTopWindow(frame)

if __name__ == '__main__':
    a = A(
        redirect=False,
        filename=None,
        useBestVisual=True)
    a.MainLoop()
