import wx
import circe_globals
import wx.html as html

ID_SEARCH_CTRL = wx.NewId()

class HelpDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "%s Help Browser" % (circe_globals.APPNAME), wx.DefaultPosition, wx.DefaultSize)

        self.notebook = wx.Notebook(self, -1, size=(100,110))

        self.index_tab = wx.Panel(self.notebook)
        self.search_tab = wx.Panel(self.notebook)                

        self.notebook.AddPage(self.index_tab, "Index")
        self.notebook.AddPage(self.search_tab, "Search")

        self.index_sizer = wx.FlexGridSizer(1,2)
        self.index_tab.SetSizer(self.index_sizer)

        self.search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.search_tab.SetSizer(self.search_sizer)
 
        self.index_tree = wx.ListCtrl(self.index_tab,ID_SEARCH_CTRL,size=(75, 220))
        self.index_sizer.Add(self.index_tree,1)
        self.index_tree.InsertColumn(0, "Topics")
        self.index_tree.Append(("Welcome To Circe",))

        text = "<b>Welcome To Circe Help Browser.</b><br />"
        self.init_html_win(self.index_tab, self.index_sizer)
        self.set_html_win(text)

    def init_html_win(self, parent, sizer):
        self.html = html.HtmlWindow(parent, -1, size=(320, 220))
        sizer.Add(self.html, 2)
    def set_html_win(self, html):
        self.html.SetPage(html)