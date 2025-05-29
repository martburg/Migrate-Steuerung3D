import wx
import time
import subprocess
from panda3d.core import loadPrcFileData, WindowProperties
from direct.showbase.ShowBase import ShowBase
from wx import xrc
import shlex

# === Configure Panda3D ===
loadPrcFileData("", "window-type none")
loadPrcFileData("", "audio-library-name null")


class MyFrame(wx.Frame):
    def __init__(self):
        #style = wx.DEFAULT_FRAME_STYLE & ~wx.MINIMIZE_BOX
        super().__init__(None, title="3DSteuerung Modern", size=(800, 600))

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

        # --- Top panel ---
        self.top_panel = wx.Panel(self, style=wx.BORDER_SIMPLE)
        self.top_panel.SetBackgroundColour("#e0e0ff")

        # --- Vertical splitter (middle + bottom), direct child of frame ---
        self.middle_and_bottom_splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)

        # --- Horizontal splitter (left+center + right), child of vertical splitter ---
        self.left_center_right_splitter = wx.SplitterWindow(self.middle_and_bottom_splitter, style=wx.SP_LIVE_UPDATE)

        # --- Inner horizontal splitter: left + center ---
        self.lr_splitter = wx.SplitterWindow(self.left_center_right_splitter, style=wx.SP_LIVE_UPDATE)
        left_panel   = wx.Panel(self.lr_splitter, style=wx.BORDER_SIMPLE)
        center_panel = wx.Panel(self.lr_splitter, style=wx.BORDER_SIMPLE)
        left_panel.SetBackgroundColour("#d0d0d0")
        center_panel.SetBackgroundColour("#ffffff")  # Panda3D goes here
        self.lr_splitter.SplitVertically(left_panel, center_panel, sashPosition=150)

        # --- Right panel, direct child of left_center_right_splitter ---
        right_panel = wx.Panel(self.left_center_right_splitter, style=wx.BORDER_SIMPLE)
        right_panel.SetBackgroundColour("#d0d0d0")

        self.left_center_right_splitter.SplitVertically(self.lr_splitter, right_panel, sashPosition=650)

        # --- Bottom panel, direct child of middle_and_bottom_splitter ---
        self.bottom_panel = wx.Panel(self.middle_and_bottom_splitter, style=wx.BORDER_SIMPLE)
        self.bottom_panel.SetBackgroundColour("#ffe0e0")

        self.middle_and_bottom_splitter.SplitHorizontally(self.left_center_right_splitter, self.bottom_panel, sashPosition=500)

        # --- Main vertical sizer for frame ---
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.top_panel, 1, wx.EXPAND | wx.ALL, 2)
        main_sizer.Add(self.middle_and_bottom_splitter, 10, wx.EXPAND, 0)
        self.SetSizer(main_sizer)

        # Reference for Panda3D integration
        self.center_panel = center_panel
    def on_resize(self, event):
        self.Layout()
        event.Skip()

class WxIntegration:
    def __init__(self, panda_window_handle=None, set_focus_func=None):
        self.panda_window_handle = panda_window_handle
        self.set_focus_func = set_focus_func

    def step(self, task=None):
        if self.set_focus_func and self.panda_window_handle:
            self.set_focus_func(self.panda_window_handle)

        wx.GetApp().ProcessPendingEvents()
        time.sleep(0.001)  # Throttle to prevent high CPU

        return task.cont if task else None

class PandaWxApp:
    def __init__(self):

        self.focus_check_counter = 0
        self._wx_focused = False
        self._wx_iconized = False
        self.panda_visible = True
        self.base = ShowBase()
        self.base.startWx()
        self.app = self.base.wxApp

        self.frame  = MyFrame()
        self.panel = self.frame.center_panel
        self.frame.Show()

        self.init_panda_window()

        self.panel.Bind(wx.EVT_SIZE, self.on_resize)
        self.frame.Bind(wx.EVT_MOVE, self.on_move)
        self.frame.Bind(wx.EVT_SIZE, self.on_resize)
        self.frame.Bind(wx.EVT_ICONIZE, self.on_iconize)

        wx.CallLater(200, self.delayed_sync)

        self.wx_loop = WxIntegration(
            panda_window_handle=self.base.win.getWindowHandle().getIntHandle(),
            set_focus_func=self.set_window_focus  # or None
        )
        
        self.base.taskMgr.add(self.wx_loop.step, "WxEventLoop")
        self.base.taskMgr.doMethodLater(0.5, self.focus_check_task, "FocusCheck")

    def set_window_focus(self,handle):
        pass  # Implement this function to set focus to the Panda3D window

    def init_panda_window(self):
        props = WindowProperties()
        props.setUndecorated(True)
        props.setOrigin(0, 0)
        props.setSize(800, 600)
        props.setTitle("PandaInWx")
        self.base.openWindow(props=props)

        model = self.base.loader.loadModel("panda")
        model.reparentTo(self.base.render)
        self.base.camera.setPos(0, -50, 10)

    def sync_window(self):
        pos = self.panel.ClientToScreen((0, 0))
        size = self.panel.GetSize()
        props = WindowProperties()
        props.setOrigin(pos.x, pos.y)
        props.setSize(size.width, size.height)
        self.base.win.requestProperties(props)

    def lift_window(self):
        handle = self.base.win.getWindowHandle().getIntHandle()
        if handle:
            hex_id = hex(handle)
            try:
                subprocess.run(["wmctrl", "-i", "-r", hex_id, "-b", "add,above"])
                subprocess.run(["wmctrl", "-i", "-a", hex_id])
            except Exception as e:
                print("wmctrl failed:", e)

    def on_iconize(self, event):
        if event.IsIconized():
            print("🔻 WX minimized → Hiding Panda window")
            self.hide_panda_window()
        else:
            print("🔼 WX restored → Showing Panda window")
            wx.CallLater(200, self.restore_and_lift_panda)
        event.Skip()

    def hide_panda_window_A(self):
        props = WindowProperties()
        props.setMinimized(True)
        self.base.win.requestProperties(props)

    def restore_and_lift_panda_A(self):
        props = WindowProperties()
        props.setMinimized(False)
        self.base.win.requestProperties(props)
        wx.CallLater(200, self.lift_window)  # Give it time to unminimize

    def hide_panda_window(self):
        # Move far off-screen to simulate minimization
        props = WindowProperties()
        props.setOrigin(-2000, -2000)
        props.setSize(1, 1)  # Optionally shrink to nearly nothing
        self.base.win.requestProperties(props)

    def restore_and_lift_panda(self):
        self.sync_window()
        wx.CallLater(200, self.lift_window)

    def delayed_sync(self):
        self.sync_window()
        self.lift_window()

    def on_resize(self, event):
        self.sync_window()
        self.lift_window()
        event.Skip()

    def on_move(self, event):
        self.sync_window()
        self.lift_window()
        event.Skip()

    def get_focused_window_id(self):
        try:
            output = subprocess.check_output(
                shlex.split("xprop -root _NET_ACTIVE_WINDOW"), stderr=subprocess.DEVNULL
            ).decode()
            # Example output: _NET_ACTIVE_WINDOW(WINDOW): window id # 0x3a00007
            if "window id #" in output:
                hex_id = output.strip().split()[-1]
                return int(hex_id, 16)
        except Exception as e:
            print("focus check failed:", e)
        return None

    def focus_check_task(self, task):
        self.focus_check_counter += 1
        print("👁 Checking focus...",self.focus_check_counter)
        try:
            panda_id = self.base.win.getWindowHandle().getIntHandle()
            focused_id = self.get_focused_window_id()
            if focused_id != panda_id and self.panda_visible:
                print("👁 Focus lost → Hiding Panda")
                self.hide_panda_window()
                self.panda_visible = False
            elif focused_id == panda_id and not self.panda_visible:
                print("👁 Focus regained → Showing Panda")
                self.restore_and_lift_panda()
                self.panda_visible = True
            return task.again
        except Exception as e:
            print ("Focus check error:", e)
            return task.done


    def run(self):
        self.base.run()

if __name__ == "__main__":
    app = PandaWxApp()
    app.run()
