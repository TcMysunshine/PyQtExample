from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QLineEdit, QToolBar, QAction, QMainWindow
from PyQt5.QtGui import *
import sys


class BrowserWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(BrowserWidget, self).__init__(*args, **kwargs)
        # self.setWindowTitle("自制浏览器")
        self.resize(800, 600)
        #一定要加self不然不会显示，指明父类
        self.layout = QVBoxLayout(self)
        #浏览器
        self.browser = MyWebEngiew()
        url = "https://www.baidu.com/"
        self.browser.setUrl(QUrl(url))
        #url 地址栏
        self.urlbar = QLineEdit()
        self.urlbar.setText(url)
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        #导航栏
        # navigation_bar = QToolBar('Navigation')
        # navigation_bar.setIconSize(QSize(16, 16))
        self.navigate_bar = QToolBar("Navigate")
        self.navigate_bar.addAction(QAction("Back", self.layout, triggered=self.browser.back))
        self.navigate_bar.addAction(QAction("Stop", self.layout, triggered=self.browser.stop))
        self.navigate_bar.addAction(QAction("Forward", self.layout, triggered=self.browser.forward))
        self.navigate_bar.addAction(QAction("Reload", self.layout, triggered=self.browser.reload))
        #添加
        self.layout.addWidget(self.urlbar)
        self.layout.addWidget(self.navigate_bar)
        self.layout.addWidget(self.browser)
        self.browser.urlChanged.connect(self.updateUrlBar)

    def navigate_to_url(self):
        # print(self.urlbar.text())
        q = QUrl(self.urlbar.text())
        # print(q.scheme())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)

    def updateUrlBar(self, new_url):
        self.urlbar.setText(new_url.toString())
        #光标指向最初的地方，不然地址太长
        self.urlbar.setCursorPosition(0)


class MyWebEngiew(QWebEngineView):
    def createWindow(self, type: QWebEnginePage.WebWindowType):
        return self

    # windowList = []
    #
    # def createWindow(self, type: QWebEnginePage.WebWindowType):
    #     new_browser = QWebEngineView()
    #     new_widget = BrowserWidget()
    #     new_widget.layout.addWidget(new_browser)
    #     self.windowList.append(new_widget)
    #     return new_browser


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bw = BrowserWidget()
    bw.show()
    sys.exit(app.exec_())
