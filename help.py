# -*- coding: utf-8 -*- 

import wx
import wx.html
###########################################################################
## Class help_frame
###########################################################################

class help_frame ( wx.Frame ):
    
    def __init__( self ):
        wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Data Quality -- Справка", pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.CAPTION|wx.SYSTEM_MENU|wx.ALWAYS_SHOW_SB )
        
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
        
        self.html_page = self.CreateHTMLCtrl(self.m_panel3)
        
        self.html_page.SetPage(start_text)
        bSizer4.Add( self.html_page, 1, wx.EXPAND, 5 )
        
        self.m_panel3.SetSizer( bSizer4 )
        self.m_panel3.Layout()
        bSizer4.Fit( self.m_panel3 )
        self.m_splitter1.SplitVertically( self.m_panel2, self.m_panel3, 214 )
        bSizer1.Add( self.m_splitter1, 1, wx.EXPAND, 5 )
        

        self.SetSizer( bSizer1 )
        self.Layout()
        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu1 = wx.Menu()
        self.exit_menuitem = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Выход\tCtrl+Q", wx.EmptyString, wx.ITEM_NORMAL )
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
    
    def OnSelChanged(self, event):
        item = self.tree.GetItemText(event.GetItem())
        if item == self.tree.GetItemText(self.root):
            self.html_page.SetPage(start_text)

        if item == self.tree.GetItemText(self.chConn):
            self.html_page.SetPage(connect1_text)
        if item == self.tree.GetItemText(self.EnConData):
            self.html_page.SetPage(connect2_text)
        if item == self.tree.GetItemText(self.ManagerConnection):
            self.html_page.SetPage(connect3_text)

        if item == self.tree.GetItemText(self.chDQ):
            self.html_page.SetPage(dq1_text)
        if item == self.tree.GetItemText(self.ParamsDQ):
            self.html_page.SetPage(dq2_text)
        if item == self.tree.GetItemText(self.ResultsDQ):
            self.html_page.SetPage(dq3_text)
        if item == self.tree.GetItemText(self.ReportDQ):
            self.html_page.SetPage(dq4_text)

        if item == self.tree.GetItemText(self.chRegexp):
            self.html_page.SetPage(regexp1_text)
        if item == self.tree.GetItemText(self.EnRegexps):
            self.html_page.SetPage(regexp2_text)
        if item == self.tree.GetItemText(self.DeRegexps):
            self.html_page.SetPage(regexp3_text)
        if item == self.tree.GetItemText(self.ChParams):
            self.html_page.SetPage(regexp4_text)
        
        if item == self.tree.GetItemText(self.chJour):
            self.html_page.SetPage(journa1_text)

    def OnExit(self, event):
        self.Destroy()
 
    def m_splitter1OnIdle( self, event ):
        self.m_splitter1.SetSashPosition( 214 )
        self.m_splitter1.Unbind( wx.EVT_IDLE )
    
    
    def CreateHTMLCtrl(self, parent=None):
        if not parent:
            parent = self

        ctrl = wx.html.HtmlWindow(parent, -1, wx.DefaultPosition, wx.Size(400, 300))
        return ctrl

start_text = \
'<b>"Data Quality" -- Приложение для оценки качества данных</b>'\
'<div><br />' \
'<div>Добро пожаловать в справку по приложению Data Quality. Здесь рассмотрены основные аспекты работы с программой. Такие как:<ul>'  \
'<li>Подключение к базе данных Oracle с использованием менеджера подключений. </li>'  \
'<li>Работа с инструментом ввода/отладки регулярных выражений для последующей оценки качества данных.</li>' \
'<li>Процесс оценки качества данных</li></ul></div></div>' \

connect1_text = \
'<b>"Data Quality" -- Подключение к базе данных Oracle<br /></b>' \
'<div><br />' \
'<div>' \
'<div>Система соединения с базой данных Oracle предусматривает два этапа:</div></div></div>' \
'<div><br /></div>' \
'<div>' \
'<ol>' \
'<li>Ввод данных для подключения</li>' \
'<li>Выбор подключения в менеджере подключений</li></ol></div>' \

connect2_text = \
'<b>"Data Quality" -- Информация для соединения с базой данных</b>' \
'<div><br />' \
'<div>' \
'<img src="/data/img/help/con_1.png" border="0">' \
'<div>При создании нового подключения в менеджере подключений возникнет окно с формами для заполнения:</div>' \
'<div><br /></div>' \
'<div>1. Имя соединения</div>' \
'<div>Произвольное имя соединения, преимущественно оно должно асоциироваться с сервером к которому будет происходить подключение.</div>' \
'<div><br /></div>' \
'<div>2. Имя</div>' \
'<div>В данное поле необходимо напечатать имя которое Вы используете непосредственно для подключения к базе данных к которой будет происходить подключение.</div>' \
'<div><br /></div>' \
'<div>3. Пароль</div>' \
'<div>В данное поле необходимо напечатать пароль который Вы используете непосредственно для подключения к базе данных к которой будет происходить подключение.</div>' \
'<div><br /></div>' \
'<div>4. IP адрес</div>' \
'<div>В данное поле следует ввести IP адрес где находится сервер. Данную информацию следует получить у системного администратора Вашей сети.</div>' \
'<div><br /></div>' \
'<div>5. Порт</div>' \
'<div>Порт, на котором находится TNS Listener. Данную информацию следует уточнить у системного администратора базы данных.</div>' \
'<div><br /></div>' \
'<div>6,7. SID, Имя сервиса</div>' \
'<div>SID - Cистемный Идентификатор Базы Данных (System Identifier). Хранится в переменной среды ORACLE_SID и используется утилитами и сетевыми компонентами для доступа к базе данных. Имя службы (Service Name). Service Name определяет одно или ряд имен для подключения к одному экземпляру базы данных. Возможные значения SERVICE_NAME указываются в сетевых установках Oracle и регистрируются в качестве службы БД процессом listener. Стандартный способ получения SID и SERVICE_NAME, который работал до десятой версии СУБД Oracle &amp;ndash; это использование утилиты lsnrctl. Для этого достаточно воспользоваться командой services: LSNRCTL&amp;gt; services . Данную информацию следует уточнить у администатора базы данных.</div>' \
'<div><br /></div>' \
'<div>Дополнительная опция "Сохранить пароль?". Если поставить галочку, то пароль сохранится для данного соединения и программа будет соединятся без запроса пароля. В ином случае, при соединении с базой каждый раз будет запрошен пароль к базе данных.</div></div></div>' \

connect3_text = \
'<b>"Data Quality" -- Менеджер подключений</b>' \
'<div><b><br /></b>' \
'<div>' \
'<div>' \
'<div>В приложении есть свой менеджер подключений, что облегчает задачу подключения к разным базам данных Oracle, подключение с различными вводными данными.</div></div></div>' \
'<div><br /></div>' \
'<img src="/data/img/help/con_2.png" border="0">' \
'<div><br /></div>' \
'<div>Все подключение отображаются в выпадающем меню. Есть возможность создания большого количества подключений с различными, уникальными именами (возможности существования двух одинаковых имен подключений не возможна, в случае создания нового подключения с именем, которое уже существует, старое подключение&nbsp;перезапишется&nbsp;с новыми данными, как будто Вы его отредактировали), также можно редактировать подключение, в случае если Вы ошиблись в вводе данных или же данные изменились.&nbsp;</div>' \
'<div><br /></div>' \
'<div>Нажав на кнопку "Помощь", Вы попадаете в этот раздел справки.</div>' \
'<div><br /></div>' \
'<div><b>ВНИМАНИЕ:</b> В ситуации, когда Вы начали редактировать соединение с базой данных, а пароль вы изначально сохранили (поставили галку "Сохранить пароль?"), то при редактировании соединения, в случае сохранения изменений, галку необходимо будет поставить заново.</div></div>' \
'<div><br /></div>' \
'<div><br /></div>' \
'<div><br /></div>' \

dq1_text = \
'<b>"Data Quality" -- Процесс оценки качества данных</b>' \
'<div><b><br /></b></div>' \
'<div>Данный раздел справки рассказывает о этапах процесса оценки качества данных. Для начала процесса оценки качества данных необходимо пройти несколько этапов:</div>' \
'<div>' \
'<ol>' \
'<li>Выбор параметров на основе коих будет происходить процесс оценки качества данных</li>' \
'<li>Результаты оценки качества данных</li>' \
'<li>Формирование отчета по результатам оценки качества данных</li></ol>' \
'<div><b><br /></b>' \
'<div>' \
'<div>' \
'<div><br /></div></div></div></div>' \
'<div><br /></div>' \
'<div><br /></div></div>' \

dq2_text = \
'<b>"Data Quality" -- Параметры оценки качества данных</b>' \
'<div><b><br /></b></div>' \
'<div>Всего для оценки качества данных используется 11 параметров:</div>' \
'<div><br /></div>' \
'<div>' \
'<ol>' \
'<li>Пустые значения - значения нулевой длины.</li>' \
'<li>Не несущие информацию значения - не несущие значимой информации значения касательно анализируемых данных.</li>' \
'<li>Не соответствующие формату значения - параметр следует использовать для тех значений, для которых имеет значение формат имеющихся данных, для проверки&nbsp;соответствия.</li>' \
'<li>Значение уровня шума - уровнем шума может считаться что угодно касательно оцениваемых данных, любые лишние, не информационные символы "внутри" данных.</li>' \
'<li>Идентифицируемость - сходимость&nbsp;идентифицирующих&nbsp;данных с имеющимися.</li>' \
'<li>Согласованность - согласованность данных с&nbsp;имеющимися&nbsp;данными.</li>' \
'<li>Унификация - уникальность значений, необходимо применять где данный фактор имеет большое влияние для качества данных.</li>' \
'<li>Оперативность - позволяет оценить насколько данные актуальны.</li>' \
'<li>Противоречивость - нет ли диссонанса среди оцениваемых данных.</li>' \
'<li>Степень классификации -</li>' \
'<li>Степень структуризации -&nbsp;</li></ol></div>' \
'<div>' \
'<div><b><br /></b>' \
'<div>' \
'<div>На изображении сверху изображено окно выбора параметров для оценки качества данных. </div>' \
'<div>На данном окне присутствуют такие элементы как выпадающий список со всеми возможными параметрами для оценки, поле для ввода весового коэффициента для выбранного параметра и чекбокс для непосредственного выбора параметра. <div>' \
'<div>Последовательность действий следующая:</div>' \
'<div>' \
'<ol>' \
'<li>Выбор параметра из выпадающего списка</li>' \
'<li>Ввод весового коэффициента для выбранного параметра</li>' \
'<li>Отметка чекбокса "Использовать параметр" для подтверждения</li>' \
'</ol> </div>' \
'<div>Параметр "Степень классификации требует дополнительных данных - количество справочников, используемых в выбранной таблице. Скажем в таблице есть три поля: ID, NAMEU, ADRESS и поле ADRESS заполнено используя справочник, а остальные нет. В этом случае число используемых справочников будет равняться единице.</div>' \
'<div> </div>' \
'<div>' \
'<div><br /></div></div></div></div>' \
'<div><br /></div>' \
'<div><br /></div></div>' \

dq3_text = \
'<b>"Data Quality" -- Резльтута оценки качества данных</b>' \
'<div><b><br /></b></div>' \
'<div><br /></div>' \
'<div>' \
'As soon as possible :D'

dq4_text = \
'<b>"Data Quality" -- Отчет об оценке качества данных</b>' \
'<div><b><br /></b></div>' \
'<div>Для каждого результата предусмотрена функция формирования отчета, включающая в себя: Основную статистику, Расширенную статистику (если в оценке использовались параметры для которых есть расширенная статистика) и советы по улучшению качества данных.</div>' \
'<div>Все отчеты формируются автоматически в каталоге reports, на основе заранее заданного шаблона с использованием HTML и CSS. В случае если есть необходимость в видоизменении отчетов - обратитесь к Вашему системному администратору. </div>'

'<div><br /></div>' \
'<div>' \