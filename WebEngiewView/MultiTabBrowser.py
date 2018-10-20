from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, QSize
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QLineEdit, QToolBar, QAction, QMainWindow, QTabWidget
from PyQt5.QtGui import *
import sys


class MultiTabBrowser(QtWidgets.QWidget):
    def __init__(self, Form):
        Form.resize(900, 700)
        # 初始化tab页
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabShape(QTabWidget.Triangular)

        self.tabWidget.tabCloseRequested.connect(self.tabWidget.removeTab)
        self.tabWidget.setGeometry(0, 0, 900, 650)
        #浏览器
        url = "http://www.baidu.com"
        self.browser = MyBrowser(self)
        self.browser.setUrl(QUrl(url))
        self.createWebView(self.browser)
    #创建浏览器Tab页
    def createWebView(self, webView):
        # self.tab = QtWidgets.QWidget()
        self.tabWidget.addTab(webView, "新标签页")
        self.tabWidget.setCurrentWidget(webView)
        #
        # self.layout = QtWidgets.QHBoxLayout(self.tab)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.addWidget(webView)

    #关闭tab页
    # def close_tab(self, index):
    #     print(index)
    #     if self.tabWidget.count() > 1:
    #         self.tabWidget.removeTab(index)
    #     else:
    #         self.close()


class MyBrowser(QWebEngineView):
    def __init__(self, widget, parent=None):
        super(MyBrowser, self).__init__(parent)
        self.widget = widget

    def createWindow(self, type: QWebEnginePage.WebWindowType):
        new_browser = MyBrowser(self.widget)
        self.widget.createWebView(new_browser)
        return new_browser


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.setCentralWidget(MultiTabBrowser(self))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    bw = MultiTabBrowser(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
