import wx
import wx.xrc
import wx.lib.mixins.listctrl as listmix

class listKeyPoints(wx.ListCtrl, listmix.TextEditMixin):
    def __init__(self):
        super().__init__()
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def _PostInit(self):
        listmix.TextEditMixin.__init__(self)
        self.DeleteAllColumns()
        self.InsertColumn(0, 'Description', format=wx.LIST_FORMAT_LEFT, width=80)
        self.InsertColumn(1, 'Number', format=wx.LIST_FORMAT_CENTER, width=55)
        self.InsertColumn(2, 'X-Coord', format=wx.LIST_FORMAT_CENTER, width=60)
        self.InsertColumn(3, 'Y-Coord', format=wx.LIST_FORMAT_CENTER, width=60)
        self.InsertColumn(4, 'Z-Coord', format=wx.LIST_FORMAT_CENTER, width=60)
        self.InsertColumn(5, 'Time', format=wx.LIST_FORMAT_CENTER, width=60)
        self.InsertColumn(6, 'Vx', format=wx.LIST_FORMAT_CENTER, width=60)
        self.InsertColumn(7, 'Vy', format=wx.LIST_FORMAT_CENTER, width=60)
        self.InsertColumn(8, 'Vz', format=wx.LIST_FORMAT_CENTER, width=60)
        self.InsertColumn(9, 'VAbs', format=wx.LIST_FORMAT_CENTER, width=60)

    def OnCreate(self, evt):
        self.Unbind(wx.EVT_WINDOW_CREATE)
        self._PostInit()
        self.Refresh()


class listBigKeyPoints(wx.ListCtrl, listmix.TextEditMixin):
    def __init__(self):
        super().__init__()
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def _PostInit(self):
        listmix.TextEditMixin.__init__(self)

    def OnCreate(self, evt):
        self.Unbind(wx.EVT_WINDOW_CREATE)
        self._PostInit()
        self.Refresh()


class listKeyPointWindow(wx.ListCtrl, listmix.TextEditMixin):
    def __init__(self):
        super().__init__()
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def _PostInit(self):
        listmix.TextEditMixin.__init__(self)

    def OnCreate(self, evt):
        self.Unbind(wx.EVT_WINDOW_CREATE)
        self._PostInit()
        self.Refresh()


class listPathEditWindow(wx.ListCtrl, listmix.TextEditMixin):
    def __init__(self):
        super().__init__()
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def _PostInit(self):
        listmix.TextEditMixin.__init__(self)

    def OnCreate(self, evt):
        self.Unbind(wx.EVT_WINDOW_CREATE)
        self._PostInit()
        self.Refresh()
