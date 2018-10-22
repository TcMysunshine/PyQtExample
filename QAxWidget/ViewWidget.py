# from PyQt5.QAxContainer import QAxWidget
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import QVariant
# from PyQt5.QtWidgets import QApplication
# import sys
# from win32com import client as wc
# from win32com.client import Dispatch, constants, gencache
# #嵌入word
# class ViewWidget(QWidget):
#
#     def __init__(self, filePath):
#         super(ViewWidget, self).__init__()
#         self.filePath = filePath
#         # self.resize(800, 600)
#         self.layout = QVBoxLayout(self)
#         self.axWidget = QAxWidget(self)
#         # self.axWidget.setRead
#         # self.axWidget.resize(700, 500)
#         self.getViewWidget()
#
#     def getViewWidget(self):
#         dot_index = self.filePath.rindex(".")
#         extension = self.filePath[dot_index:]
#         if extension.find('.doc') > -1:
#             return self.getWordView()
#         else:
#             return self.getPdfView()
#
#     def getWordView(self):
#         # self.axWidget.clear()
#         if not self.axWidget.setControl("Word.Application"):
#             print("未安装Word")
#         # self.axWidget.dynamicCall("SetVisible (bool Visible)", "false")
#         self.axWidget.setProperty('DisplayAlerts', False)
#         self.axWidget.setProperty("DisplayScrollBars", True)
#         self.axWidget.setProperty("Visible", False)
#         self.axWidget.setControl(self.filePath)
#         self.layout.addWidget(self.axWidget)
#
#     def getPdfView(self):
#         self.axWidget.clear()
#         self.axWidget = QAxWidget("Microsoft Web Browser")
#         self.axWidget.dynamicCall("Navigate(const QString&)", self.filePath)
#         self.axWidget.setProperty("DisplayAlerts", False)
#         self.layout.addWidget(self.axWidget)
#
#     def closeEvent(self, event):
#         self.axWidget.close()
#         self.axWidget.clear()
#         self.layout.removeWidget(self.axWidget)
#         del self.axWidget
#         super(ViewWidget, self).closeEvent(event)
#
#     def getFileName(self):
#         last_index = self.filePath.rindex("/")
#         return self.filePath[last_index+1:]
#
#
# #word转pdf 其他的都一样都是利用win32调用word,ppt来转换
# def word2pdf(wordFile, pdfFile):
#     word = gencache.EnsureDispatch("Word.Application")
#     doc = word.Documents.Open(wordFile, ReadOnly = 1)
#     doc.ExportAsFixedFormat(pdfFile, constants.wdExportFormatPDF,
#                             Item=constants.wdExportDocumentWithMarkup,
#                             CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
#     word.Quit(constants.wdDoNotSaveChanges)
#
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     viewWidget = ViewWidget("E:/sltz.docx")
#     viewWidget.show()
#     sys.exit(app.exec_())