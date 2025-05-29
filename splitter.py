import wx

class SplitterFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="3DSteuerung Modern", size=(1200, 800))

        # --- Menu Bar ---
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_OPEN, "&Open")
        file_menu.Append(wx.ID_EXIT, "E&xit")
        menubar.Append(file_menu, "&File")
        self.SetMenuBar(menubar)

        # --- Status Bar ---
        self.CreateStatusBar()
        self.SetStatusText("Ready")

        # --- Outer Vertical Splitter (Left <-> RightComposite) ---
        left_splitter = wx.SplitterWindow(self)
        left_panel = wx.Panel(left_splitter)
        right_splitter = wx.SplitterWindow(outer_splitter)
        outer_splitter.SplitVertically(left_panel, right_composite, 200)

        # --- Inner Horizontal Splitter (TopComposite <-> Bottom) ---
        inner_splitter = wx.SplitterWindow(right_composite)
        top_composite = wx.Panel(right_composite)
        bottom_panel = wx.Panel(inner_splitter)
        right_composite.SplitHorizontally(top_composite, inner_splitter, 150)

        # --- Top Composite (Top <-> Center) ---
        top_splitter = wx.SplitterWindow(top_composite)
        top_panel = wx.Panel(top_splitter)
        center_panel = wx.Panel(top_splitter)
        top_splitter.SplitVertically(top_panel, center_panel, 150)

        # --- Set Parent Layouts ---
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(outer_splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # --- Panel Colors ---
        left_panel.SetBackgroundColour(wx.Colour(255, 0, 0))  
        top_panel.SetBackgroundColour(wx.Colour(0, 255, 0))   
        center_panel.SetBackgroundColour(wx.Colour(255, 255, 255)) 
        bottom_panel.SetBackgroundColour(wx.Colour(0, 0, 255))  

        # --- Splitter Config ---
        outer_splitter.SetMinimumPaneSize(100)
        right_composite.SetMinimumPaneSize(100)
        inner_splitter.SetMinimumPaneSize(100)
        top_splitter.SetMinimumPaneSize(100)

        self.Bind(wx.EVT_SIZE, self.on_resize)

    def on_resize(self, event):
        self.Layout()
        event.Skip()

if __name__ == '__main__':
    app = wx.App(False)
    frame = SplitterFrame()
    frame.Show()
    app.MainLoop()
