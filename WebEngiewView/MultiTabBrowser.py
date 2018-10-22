from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtCore import QUrl, QSize
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class MultiTabBrowser(QtWidgets.QWidget):
    def __init__(self):
        super(MultiTabBrowser, self).__init__()
        # 初始化tab页
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabShape(QTabWidget.Triangular)

        # self.tabWidget.tabCloseRequested.connect(self.tabWidget.removeTab)
        self.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.tabWidget.setGeometry(0, 0, 900, 650)
        #浏览器
        url = "http://www.baidu.com"
        self.browser = MyBrowser(self)
        self.browser.setUrl(QUrl(url))
        #网站标题改变时才会触发函数
        self.browser.titleChanged.connect(self.changeTitle)
        self.createWebView(self.browser)

    #创建浏览器Tab页
    def createWebView(self, webView):
        # self.tab = QtWidgets.QWidget()
        self.webView = webView
        self.tabWidget.addTab(self.webView, "新标签页")
        self.tabWidget.setCurrentWidget(self.webView)
        # #
        # self.layout = QtWidgets.QHBoxLayout(self.tab)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.addWidget(webView)

    #关闭tab页
    def close_tab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
        else:
            self.close()

    #改变网页标题
    def changeTitle(self):
        title = self.webView.title()
        current_index = self.tabWidget.currentIndex()
        self.tabWidget.setTabText(current_index, title)


class MyBrowser(QWebEngineView):
    def __init__(self, widget, parent=None):
        super(MyBrowser, self).__init__(parent)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)#支持页面播放
        self.page().profile().downloadRequested.connect(self.downloadRequested) # 页面下载请求
        # self.page().windowCloseRequested.connect(self.closeWindow)
        self.widget = widget

    # def closeWindow(self):
    #     index = self.widget.tabWidget.currentIndex()
    #     print(index)
    #     self.mainwindow.tabWidget.removeTab(index)
    #重写方法
    def createWindow(self, type: QWebEnginePage.WebWindowType):
        new_browser = MyBrowser(self.widget)
        new_browser.titleChanged.connect(self.widget.changeTitle)
        self.widget.createWebView(new_browser)
        return new_browser
    #下载
    def downloadRequested(self,downloadItem):
        if downloadItem.isFinished() == False and downloadItem.state() == 0:
            file_path, _ = QFileDialog.getSaveFileName(self, "save file", "", "xall files(*.*)")
             ###下载文件
            # downloadItem.setSavePageFormat(QWebEngineDownloadItem.CompleteHtmlSaveFormat)
            downloadItem.setPath(file_path)
            downloadItem.accept()
            downloadItem.finished.connect(self.downloadfinished)

    # 下载结束触发函数
    def downloadfinished(self):
        js_string = '''
           alert("下载成功，请到软件同目录下，查找下载文件！"); 
           '''
        self.page().runJavaScript(js_string)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # mainWindow = QMainWindow()
    bw = MultiTabBrowser()
    bw.show()
    # mainWindow.show()
    sys.exit(app.exec_())
