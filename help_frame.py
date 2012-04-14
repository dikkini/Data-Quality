# -*- coding: utf-8 -*- 

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class help_frame
###########################################################################

class help_frame ( wx.Frame ):
    
    def __init__( self ):
        wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Data Quality -- Справка", pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.ALWAYS_SHOW_SB )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
        
        self.m_panel2 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        
        self.tree = wx.TreeCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, (800,600), wx.TR_DEFAULT_STYLE )
        bSizer3.Add( self.tree, 0, wx.EXPAND, 5 )
        
        
        self.m_panel2.SetSizer( bSizer3 )
        self.m_panel2.Layout()
        bSizer3.Fit( self.m_panel2 )
        self.m_panel3 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer4 = wx.BoxSizer( wx.VERTICAL )
        
        self.text_ctrl = wx.richtext.RichTextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
        bSizer4.Add( self.text_ctrl, 1, wx.EXPAND, 5 )
        
        self.m_panel3.SetSizer( bSizer4 )
        self.m_panel3.Layout()
        bSizer4.Fit( self.m_panel3 )
        self.m_splitter1.SplitVertically( self.m_panel2, self.m_panel3, 214 )
        bSizer1.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
        

        self.SetSizer( bSizer1 )
        self.Layout()
        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu1 = wx.Menu()
        self.exit_menuitem = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Выход", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.AppendItem( self.exit_menuitem )
        
        self.m_menubar1.Append( self.m_menu1, u"Файл" ) 
        
        self.SetMenuBar( self.m_menubar1 )
        
        
        self.Centre( wx.BOTH )

        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        fileopenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_GO_DIR_UP,   wx.ART_OTHER, isz))

        self.tree.SetImageList(il)
        self.il = il

        self.root = self.tree.AddRoot("Data Quality")
        self.tree.SetPyData(self.root, None)
        
        
        self.chConn = self.tree.AppendItem(self.root, u"Подключение к базе данных Oracle")
        self.EnConData = self.tree.AppendItem(self.chConn, u'Информация для подключения к базе данных')
        self.ManagerConnection = self.tree.AppendItem(self.chConn, u'Менеджер соединений')
        
        self.chRegexp = self.tree.AppendItem(self.root, u"Инструмент для ввода/отладки регулярных выражений")
        self.EnRegexps = self.tree.AppendItem(self.chRegexp, u'Ввод регулярных выражений')
        self.DeRegexps = self.tree.AppendItem(self.chRegexp, u'Отладка регулярных выражений')
        self.ChParams = self.tree.AppendItem(self.chRegexp, u'Выбор параметров для оценки качества данных')
        
        self.chDQ = self.tree.AppendItem(self.root, u"Оценка качества данных") 
        self.ParamsDQ = self.tree.AppendItem(self.chDQ, u'Параметры оценки качества данных')
        self.ResultsDQ = self.tree.AppendItem(self.chDQ, u'Результаты оценки качества данных')
        self.ReportDQ = self.tree.AppendItem(self.chDQ, u'Отчет по результатам оценки качества данных')
        
        self.chJour = self.tree.AppendItem(self.root, u'Журналы')
        
        # Settings of images
        self.tree.SetItemImage(self.root, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.root, fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.tree.SetItemImage(self.chConn, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.chConn, fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.tree.SetItemImage(self.chRegexp, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.chRegexp, fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.tree.SetItemImage(self.chJour, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.chJour, fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.tree.SetItemImage(self.chDQ, fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.chDQ, fldropenidx, wx.TreeItemIcon_Expanded)
        
        self.tree.SetItemImage(self.EnConData, fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.EnConData, fileopenidx, wx.TreeItemIcon_Selected)
        
        self.tree.SetItemImage(self.ManagerConnection, fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.ManagerConnection, fileopenidx, wx.TreeItemIcon_Selected)
        
        self.tree.SetItemImage(self.EnRegexps, fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.EnRegexps, fileopenidx, wx.TreeItemIcon_Selected)
        
        self.tree.SetItemImage(self.DeRegexps, fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.DeRegexps, fileopenidx, wx.TreeItemIcon_Selected)
        
        self.tree.SetItemImage(self.ChParams, fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.ChParams, fileopenidx, wx.TreeItemIcon_Selected)
        
        self.tree.SetItemImage(self.ParamsDQ, fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.ParamsDQ, fileopenidx, wx.TreeItemIcon_Selected)
        
        self.tree.SetItemImage(self.ResultsDQ, fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.ResultsDQ, fileopenidx, wx.TreeItemIcon_Selected)
        
        self.tree.SetItemImage(self.ReportDQ, fileidx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(self.ReportDQ, fileopenidx, wx.TreeItemIcon_Selected)
        
        # Events
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind( wx.EVT_MENU, self.OnExit, id = self.exit_menuitem.GetId() )
        self.text_ctrl.CanCut()
        self.text_ctrl.CanDeleteSelection()
        self.Start()
        
    def OnSelChanged(self, event):
        item = self.tree.GetItemText(event.GetItem())
        if item == self.tree.GetItemText(self.root):
            self.Start()

        if item == self.tree.GetItemText(self.chConn):
            self.Connect_1()
        if item == self.tree.GetItemText(self.EnConData):
            self.Connect_2()
        if item == self.tree.GetItemText(self.ManagerConnection):
            self.Connect_3()

        if item == self.tree.GetItemText(self.chDQ):
            self.DQ_1()
        if item == self.tree.GetItemText(self.ParamsDQ):
            self.DQ_3()
        if item == self.tree.GetItemText(self.ResultsDQ):
            self.DQ_4()
        if item == self.tree.GetItemText(self.ReportDQ):
            self.DQ_5()

        if item == self.tree.GetItemText(self.chRegexp):
            self.Regexp_1()
        if item == self.tree.GetItemText(self.EnRegexps):
            self.Regexp_2()
        if item == self.tree.GetItemText(self.DeRegexps):
            self.Regexp_3()
        if item == self.tree.GetItemText(self.ChParams):
            self.Regexp_4()
        
        if item == self.tree.GetItemText(self.chJour):
            self.Jour_1()

    def OnExit(self, event):
        self.Destroy()
 
    def m_splitter1OnIdle( self, event ):
        self.m_splitter1.SetSashPosition( 214 )
        self.m_splitter1.Unbind( wx.EVT_IDLE )
        
    def __del__( self ):
        pass
    
    def Start(self):
        self.text_ctrl.Clear()
        # Start Screen text
        self.text_ctrl.BeginFontSize(10)
        self.text_ctrl.BeginBold()
        self.text_ctrl.WriteText(u"Data Quality -- Приложение для оценки качества данных")
        self.text_ctrl.EndFontSize()
        self.text_ctrl.EndBold()
        self.text_ctrl.Newline()
        self.text_ctrl.Newline()
        self.text_ctrl.WriteText(u'Добро пожаловать в справку по приложению Data Quality. Здесь рассмотрены основные аспекты работы с программой. Такие как:')
        
        self.text_ctrl.BeginSymbolBullet('*', 100, 60)
        self.text_ctrl.Newline()
        self.text_ctrl.WriteText(u'Подключение к базе данных Oracle с использованием менеджера подключений.')
        self.text_ctrl.EndSymbolBullet()
        
        self.text_ctrl.BeginSymbolBullet('*', 100, 60)
        self.text_ctrl.Newline()
        self.text_ctrl.WriteText(u'Работа с инструментом ввода/отладки регулярных выражений для последующей оценки качества данных.')
        self.text_ctrl.EndSymbolBullet()

        self.text_ctrl.BeginSymbolBullet('*', 100, 60)
        self.text_ctrl.Newline()
        self.text_ctrl.WriteText(u"Процесс оценки качества данных")
        self.text_ctrl.EndSymbolBullet()
        
        self.text_ctrl.BeginSymbolBullet('*', 100, 60)
        self.text_ctrl.Newline()
        self.text_ctrl.EndSymbolBullet()

    def Connect_1(self):
        
        self.text_ctrl.Clear()
        # Main Connect Screen
        self.text_ctrl.BeginFontSize(10)
        self.text_ctrl.BeginBold()
        self.text_ctrl.WriteText(u"Data Quality -- Подключение к базе данных Oracle")
        self.text_ctrl.EndFontSize()
        self.text_ctrl.EndBold()
        
        self.text_ctrl.Newline()
        self.text_ctrl.Newline()
        
        self.text_ctrl.WriteText(u'Система соединения с базой данных Oracle предусматривает два этапа:')
        self.text_ctrl.Newline()
        
        self.text_ctrl.WriteText(u'Ввод данных для подключения')
        self.text_ctrl.BeginSymbolBullet('*', 100, 60)
        self.text_ctrl.Newline()
        self.text_ctrl.WriteText(u'Выбор подключения в менеджере подключений')
        self.text_ctrl.EndSymbolBullet()
        
        self.text_ctrl.BeginSymbolBullet('*', 100, 60)
        self.text_ctrl.Newline()
        self.text_ctrl.EndSymbolBullet()

    def Connect_2(self):
        self.text_ctrl.Clear()
        self.text_ctrl.BeginFontSize(10)
        self.text_ctrl.BeginBold()
        self.text_ctrl.WriteText(u"Data Quality -- Информация для соединения с базой данных")
        self.text_ctrl.EndFontSize()
        self.text_ctrl.EndBold()
        
        self.text_ctrl.Newline()
        self.text_ctrl.Newline()

        self.text_ctrl.WriteText(u"При создании нового подключения в менеджере подключений возникнет окно с формами для заполнения:")
        self.text_ctrl.Newline()
        self.text_ctrl.WriteImageFile('./data/img/help/con_2_1.jpg', wx.BITMAP_TYPE_ANY)
        self.text_ctrl.Newline()
        self.text_ctrl.BeginBold()
        self.text_ctrl.WriteText(u'1. Имя соединения. ') 
        self.text_ctrl.EndBold()
        self.text_ctrl.WriteText(u'Произвольное имя соединения, преимущественно оно должно асоциироваться с сервером к которому будет происходить подключение.')
        self.text_ctrl.Newline()
        self.text_ctrl.BeginBold()
        self.text_ctrl.WriteText(u'2. Имя. ') 
        self.text_ctrl.EndBold()
        self.text_ctrl.WriteText(u'В данное поле необходимо напечатать имя которое Вы используете непосредственно для подключения к базе данных к которой будет происходить подключение.')
        self.text_ctrl.Newline()
        self.text_ctrl.BeginBold()
        self.text_ctrl.WriteText(u'3. Пароль. ') 
        self.text_ctrl.EndBold()
        self.text_ctrl.WriteText(u'В данное поле необходимо напечатать пароль который Вы используете непосредственно для подключения к базе данных к которой будет происходить подключение.')
        self.text_ctrl.Newline()
        self.text_ctrl.BeginBold()
        self.text_ctrl.WriteText(u'4. IP адрес. ') 
        self.text_ctrl.EndBold()
        self.text_ctrl.WriteText(u'В данное поле следует ввести IP адрес где находится сервер. Данную информацию следует получить у системного администратора Вашей сети.')
        self.text_ctrl.Newline()
        self.text_ctrl.BeginBold()
        self.text_ctrl.WriteText(u'5. Порт. ') 
        self.text_ctrl.EndBold()
        self.text_ctrl.WriteText(u'Порт, на котором находится TNS Listener. Данную информацию следует уточнить у системного администратора базы данных.')
        self.text_ctrl.Newline()
        self.text_ctrl.BeginBold()
        self.text_ctrl.WriteText(u'6,7. SID, Имя сервиса. ') 
        self.text_ctrl.EndBold()
        self.text_ctrl.WriteText(u'SID - Cистемный Идентификатор Базы Данных (System Identifier). Хранится в переменной среды ORACLE_SID и используется утилитами и сетевыми компонентами для доступа к базе данных.') 
        self.text_ctrl.WriteText(u' Имя службы (Service Name). Service Name определяет одно или ряд имен для подключения к одному экземпляру базы данных. Возможные значения SERVICE_NAME указываются в сетевых установках Oracle и регистрируются в качестве службы БД процессом listener.')
        self.text_ctrl.WriteText(u' Стандартный способ получения SID и SERVICE_NAME, который работал до десятой версии СУБД Oracle – это использование утилиты lsnrctl. Для этого достаточно воспользоваться командой services: LSNRCTL> services . Данную информацию следует уточнить у администатора базы данных.')
        self.text_ctrl.Newline()
        self.text_ctrl.WriteText(u'Дополнительная опция "Сохранить пароль?". Если поставить галочку, то пароль сохранится для данного соединения и программа будет соединятся без запроса пароля. В ином случае, при соединении с базой каждый раз будет запрошен пароль к базе данных.')
    
    def Connect_3(self):
        self.text_ctrl.Clear()

    def Regexp_1(self):
        self.text_ctrl.Clear()
        self.text_ctrl.WriteText(u'А здесь все про инструмент ввода вывода регулярных выражений')

    def Regexp_2(self):
        self.text_ctrl.Clear()

    def Regexp_3(self):
        self.text_ctrl.Clear()

    def Regexp_4(self):
        self.text_ctrl.Clear()
  
    def DQ_1(self):
        self.text_ctrl.Clear()
        self.text_ctrl.WriteText(u'Здесь все про процесс оценки качества данных')

    def DQ_2(self):
        self.text_ctrl.Clear()

    def DQ_3(self):
        self.text_ctrl.Clear()
    
    def DQ_4(self):
        self.text_ctrl.Clear()
    
    def DQ_5(self):
        self.text_ctrl.Clear()

    def Jour_1(self):
        self.text_ctrl.Clear()