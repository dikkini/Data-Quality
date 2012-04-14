# -*- coding: utf-8 -*- 

import wx
import wx.xrc

###########################################################################
## Class about
###########################################################################

#noinspection PyArgumentList
class about ( wx.Frame ):

	"""

	"""

	def __init__( self ):
		wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = u"Data Quality -- О программе", pos = wx.DefaultPosition, size = wx.Size( 386,161 ), style = wx.CAPTION|wx.STAY_ON_TOP|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )

		self.m_panel1 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer3 = wx.GridBagSizer( 0, 0 )
		gbSizer3.SetFlexibleDirection( wx.BOTH )
		gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_bitmap5 = wx.StaticBitmap( self.m_panel1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer3.Add( self.m_bitmap5, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText11 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Data Quality", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( 100 )
		self.m_staticText11.SetFont( wx.Font( 18, 74, 90, 92, False, "Tahoma" ) )

		gbSizer3.Add( self.m_staticText11, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText29 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Версия 0.3", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )
		self.m_staticText29.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )

		gbSizer3.Add( self.m_staticText29, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


		self.m_panel1.SetSizer( gbSizer3 )
		self.m_panel1.Layout()
		gbSizer3.Fit( self.m_panel1 )
		self.m_panel4 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText30 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Программа для оценки качества данных в структурированных", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )
		self.m_staticText30.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )

		bSizer5.Add( self.m_staticText30, 0, wx.ALL, 5 )

		self.m_staticText31 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"информационных массивах.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		self.m_staticText31.SetFont( wx.Font( 10, 74, 90, 90, False, "Tahoma" ) )

		bSizer5.Add( self.m_staticText31, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		self.exit_btn = wx.Button( self.m_panel4, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.exit_btn.SetDefault() 
		bSizer7.Add( self.exit_btn, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer5.Add( bSizer7, 1, wx.EXPAND, 5 )


		self.m_panel4.SetSizer( bSizer5 )
		self.m_panel4.Layout()
		bSizer5.Fit( self.m_panel4 )
		self.m_splitter1.SplitHorizontally( self.m_panel1, self.m_panel4, 39 )
		bSizer1.Add( self.m_splitter1, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.exit_btn.Bind( wx.EVT_BUTTON, self.OnExit )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnExit( self, event ):
		self.Destroy()
		event.Skip()

	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 39 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )


