import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
import math


class PageView(QWidget):

    def __init__(self, data, titles, keys, dataRow=10, dataCol=4):
        super(PageView, self).__init__()
        self.resize(960, 790)
        #当前页数
        self.currentPage = 1
        #列数
        self.dataCol = dataCol
        #每一页展示数据行数
        self.dataRow = dataRow
        #height
        self.height = self.dataRow * 70
        # 每一列的标题
        self.titles = titles
        self.titles.append("操作")
        #数据中的key
        self.keys = keys
        # 总数据
        self.data = data
        # 获取数据长度
        self.length = len(data)
        # 获取数据可分的页数
        # //向上取整， /是得到小数
        self.pageNum = math.ceil((self.length / self.dataRow))
        # print(str(self.length) + ":" + str(self.dataRow)+":"+str(self.pageNum))
        #建立UI
        self.setUpUI()

    def setUpUI(self):
        # 上一页
        self.preButton = QPushButton("上一页", self)
        self.preButton.setGeometry(QtCore.QRect(800, self.height + 10, 50, 20))
        self.preButton.clicked.connect(self.backToLastPage)
        # 下一页
        self.nextButton = QPushButton("下一页", self)
        self.nextButton.setGeometry(QtCore.QRect(860, self.height + 10, 50, 20))
        self.nextButton.clicked.connect(self.forwardToNextPage)
        # 总页数
        self.totalPageLabel = QLabel(self)
        self.totalPageLabel.setGeometry(QtCore.QRect(640, self.height + 10, 60, 20))
        self.totalPageLabel.setText("总共" + str(self.pageNum) + "页")
        # 当前页
        self.currentPageLabel = QLabel(self)
        self.currentPageLabel.setGeometry(QtCore.QRect(700, self.height + 10, 60, 20))
        self.currentPageLabel.setText("当前第" + str(self.currentPage) + "页")
        # 转到第几页
        self.label1 = QLabel(self)
        self.label1.setGeometry(QtCore.QRect(760, self.height + 40, 40, 20))
        self.label1.setText("转到第")
        self.turnToPage = QLineEdit(self)
        self.turnToPage.setGeometry(QtCore.QRect(805, self.height + 40, 20, 20))
        self.turnToPage.setText(str(self.currentPage))
        # 转到第几页
        self.label1 = QLabel(self)
        self.label1.setGeometry(QtCore.QRect(825, self.height + 40, 20, 20))
        self.label1.setText("页")
        # 到达指定页
        self.targetPageButton = QPushButton("Go", self)
        self.targetPageButton.setGeometry(QtCore.QRect(860, self.height + 40, 50, 20))
        self.targetPageButton.clicked.connect(self.goToTargetPage)
        #布局
        self.layoutWidget = QWidget(self)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 950, self.height))
        self.layout = QVBoxLayout(self.layoutWidget)

    #返回上一页
    def backToLastPage(self):
        # print("previous")
        self.currentPage -= 1
        if self.currentPage <= 0:
            # print("到达第一页")
            QMessageBox.warning(self, "提示", "当前已是第一页")
            self.currentPage = 1
        else:
            self.layout.removeWidget(self.tableView)
            # self.model.clear()
            # self.tableView.reset()
            # self.model.removeRows(0, 5)
            self.renderData()
        self.currentPageLabel.setText("当前第" + str(self.currentPage) + "页")

    #返回下一页
    def forwardToNextPage(self):
        # print("next")
        self.currentPage += 1
        #到达最后一页
        if self.currentPage >= self.pageNum + 1:
            QMessageBox.warning(self, "提示", "当前已到达最后一页")
            self.currentPage = self.pageNum
        else:
            self.layout.removeWidget(self.tableView)
            self.renderData()
        self.currentPageLabel.setText("当前第" + str(self.currentPage) + "页")

    #到达指定页
    def goToTargetPage(self):
        self.turnToPageValue = int(self.turnToPage.text())
        if self.turnToPageValue > self.pageNum or self.turnToPageValue < 1:
            QMessageBox.warning(self, "提示", "指定页不存在，超出范围")
        else:
            self.layout.removeWidget(self.tableView)
            self.currentPage = self.turnToPageValue
            # self.model.clear()
            self.renderData()
        self.currentPageLabel.setText("当前第" + str(self.currentPage) + "页")

    def renderData(self):
        #获取当前需要渲染的数据
        self.setCurrentData()
        #当前行
        rowNum = len(self.currentData)
        self.model = QStandardItemModel(rowNum, self.dataCol + 1)
        # 设置头
        self.model.setHorizontalHeaderLabels(self.titles)
        self.tableView = QTableView(self.layoutWidget)
        # height = self.dataRow * 35
        self.tableView.resize(950, self.height + 200)
        self.tableView.verticalHeader().setDefaultSectionSize(62)
        self.tableView.setColumnWidth(1, 350)
        #填充数据
        for row in range(rowNum):
            for col in range(self.dataCol):
                tempValue = self.currentData[row][self.keys[col]]
                if col > 1:
                    value = str(tempValue)[0:10]
                else:
                    value = str(tempValue)
                item = QStandardItem(value)
                # 居中显示
                item.setTextAlignment(Qt.AlignCenter)
                # 不可编辑
                item.setEditable(False)
                self.model.setItem(row, col, item)

        #填充数据
        self.tableView.setModel(self.model)
        # 水平方向标签拓展剩下的窗口部分，填满表格
        self.tableView.horizontalHeader().setStretchLastSection(True)
        # #水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #添加按钮
        for buttonRow in range(rowNum):
            index = self.model.index(buttonRow, self.dataCol)
            self.tableView.setIndexWidget(index, self.buttonForRow(self.currentData[buttonRow]['ajxh']))
        self.layout.addWidget(self.tableView)
    #点击查看按钮传递案件序号
    def viewTable(self, id):
        print(id)

    # 列表内添加按钮
    def buttonForRow(self, id):
        widget = QWidget()
        # 查看
        viewBtn = QPushButton('查看')
        viewBtn.setStyleSheet(''' text-align : center;
                                  background-color : DarkSeaGreen;
                                  height : 30px;
                                  border-style: outset;
                                  font : 13px; ''')
        # 传入参数时要加入lambda
        viewBtn.clicked.connect(lambda: self.viewTable(id))
        #布局
        hLayout = QHBoxLayout()
        hLayout.addWidget(viewBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget
    #将数据渲染表格

    # def renderTable(self):
    #     self.tableView = QTableView(self)
    #     # height = self.dataRow * 35
    #     self.tableView.resize(750, self.height)
    #     self.tableView.setModel(self.model)
    #     # 水平方向标签拓展剩下的窗口部分，填满表格
    #     self.tableView.horizontalHeader().setStretchLastSection(True)
    #     # #水平方向，表格大小拓展到适当的尺寸
    #     self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # self.tableView.se
        # self.layout.addWidget(self.tableView)
        # self.vlayout = QHBoxLayout()

        # self.layout.addWidget(self.vlayout)

    #设置当前需要展示的数据

    def setCurrentData(self):
        start = (self.currentPage - 1) * self.dataRow
        end = self.currentPage * self.dataRow
        #最后一页
        if self.currentPage == self.pageNum:
            self.currentData = self.data[start:self.length]
        elif self.currentPage < self.pageNum:
            self.currentData = self.data[start:end]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = {
        "succeed": True,
        "message": None,
        "object": [
            {
                "ajxh": 62578,
                "ah": "(2018)津民申646号",
                "ajmc": "天津市润辉建筑发展有限公司与王作录建设工程分包合同纠纷",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-02-05T16:00:00.000+0000",
                "jarq": "2018-04-23T08:16:04.000+0000"
            },
            {
                "ajxh": 62479,
                "ah": "(2018)津民终83号",
                "ajmc": "陕西瑞中贸易有限公司,天津京铁火车头足球俱乐部有限公司不当得利纠纷",
                "ajxz": "2",
                "spcx": "2",
                "spcxdz": "29",
                "baspt": "06        ",
                "larq": "2018-01-29T16:00:00.000+0000",
                "jarq": "2018-07-26T09:28:27.000+0000"
            },
            {
                "ajxh": 62376,
                "ah": "(2018)津民申583号",
                "ajmc": "张树强与南开大学人事争议",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-24T16:00:00.000+0000",
                "jarq": "2018-03-27T07:03:19.000+0000"
            },
            {
                "ajxh": 62387,
                "ah": "(2018)津民申591号",
                "ajmc": "李艳卜与天津市保安服务总公司河西分公司劳动争议",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-24T16:00:00.000+0000",
                "jarq": "2018-04-04T08:28:39.000+0000"
            },
            {
                "ajxh": 62243,
                "ah": "(2018)津民申497号",
                "ajmc": "天津金地康成投资有限公司与李睿雅劳动争议",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-22T16:00:00.000+0000",
                "jarq": "2018-04-04T08:28:19.000+0000"
            },
            {
                "ajxh": 62245,
                "ah": "(2018)津民申499号",
                "ajmc": "宋金美与天津达璞瑞科技有限公司劳动争议纠纷",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-22T16:00:00.000+0000",
                "jarq": "2018-03-27T07:02:41.000+0000"
            },
            {
                "ajxh": 62101,
                "ah": "(2018)津民申430号",
                "ajmc": "天津众起模具制造有限公司,张义宽劳动争议",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-17T16:00:00.000+0000",
                "jarq": "2018-03-27T07:02:18.000+0000"
            },
            {
                "ajxh": 62115,
                "ah": "(2018)津民申441号",
                "ajmc": "许莹,天津市弘野建筑工程有限公司,天津市塘沽海洋高新技术开发总公司建设工程施工合同纠纷",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-17T16:00:00.000+0000",
                "jarq": "2018-04-16T08:19:09.000+0000"
            },
            {
                "ajxh": 62090,
                "ah": "(2018)津民申420号",
                "ajmc": "陈志森,天津利顺德大饭店有限公司劳动争议",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-16T16:00:00.000+0000",
                "jarq": "2018-04-10T06:27:09.000+0000"
            },
            {
                "ajxh": 61755,
                "ah": "(2018)津民申206号",
                "ajmc": "白雪樱与天津市外国企业专家服务有限公司开发区分公司,天津瑞金国际学校,新地平线国际教育管理（天津）有限公司等劳动争议纠纷",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-10T16:00",
                "jarq": "2018-04-10T06:27:09.000+0000"
            },
            {
                "ajxh": 62578,
                "ah": "(2018)津民申646号",
                "ajmc": "陕西瑞中贸易有限公司,天津京铁火车头足球俱乐部有限公司不当得利纠纷",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-02-05T16:00:00.000+0000",
                "jarq": "2018-04-23T08:16:04.000+0000"
            },
            {
                "ajxh": 62479,
                "ah": "(2018)津民终83号",
                "ajmc": "天津市润辉建筑发展有限公司与王作录建设工程分包合同纠纷",
                "ajxz": "2",
                "spcx": "2",
                "spcxdz": "29",
                "baspt": "06        ",
                "larq": "2018-01-29T16:00:00.000+0000",
                "jarq": "2018-07-26T09:28:27.000+0000"
            },
            {
                "ajxh": 62376,
                "ah": "(2018)津民申583号",
                "ajmc": "张树强与南开大学人事争议",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-24T16:00:00.000+0000",
                "jarq": "2018-03-27T07:03:19.000+0000"
            },
            {
                "ajxh": 62387,
                "ah": "(2018)津民申591号",
                "ajmc": "李艳卜与天津市保安服务总公司河西分公司劳动争议",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-24T16:00:00.000+0000",
                "jarq": "2018-04-04T08:28:39.000+0000"
            },
            {
                "ajxh": 62243,
                "ah": "(2018)津民申497号",
                "ajmc": "天津金地康成投资有限公司与李睿雅劳动争议",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-22T16:00:00.000+0000",
                "jarq": "2018-04-04T08:28:19.000+0000"
            },
            {
                "ajxh": 62115,
                "ah": "(2018)津民申441号",
                "ajmc": "许莹,天津市弘野建筑工程有限公司,天津市塘沽海洋高新技术开发总公司建设工程施工合同纠纷",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-17T16:00:00.000+0000",
                "jarq": "2018-04-16T08:19:09.000+0000"
            },
            {
                "ajxh": 62245,
                "ah": "(2018)津民申499号",
                "ajmc": "宋金美与天津达璞瑞科技有限公司劳动争议纠纷",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-22T16:00:00.000+0000",
                "jarq": "2018-03-27T07:02:41.000+0000"
            },
            {
                "ajxh": 62101,
                "ah": "(2018)津民申430号",
                "ajmc": "天津众起模具制造有限公司,张义宽劳动争议",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-17T16:00:00.000+0000",
                "jarq": "2018-03-27T07:02:18.000+0000"
            },
            {
                "ajxh": 62115,
                "ah": "(2018)津民申441号",
                "ajmc": "许莹,天津市弘野建筑工程有限公司,天津市塘沽海洋高新技术开发总公司建设工程施工合同纠纷",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-17T16:00:00.000+0000",
                "jarq": "2018-04-16T08:19:09.000+0000"
            },
            {
                "ajxh": 62090,
                "ah": "(2018)津民申420号",
                "ajmc": "陈志森,天津利顺德大饭店有限公司劳动争议",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-16T16:00:00.000+0000",
                "jarq": "2018-04-10T06:27:09.000+0000"
            },
            {
                "ajxh": 61755,
                "ah": "(2018)津民申206号",
                "ajmc": "白雪樱与天津市外国企业专家服务有限公司开发区分公司,天津瑞金国际学校,新地平线国际教育管理（天津）有限公司等劳动争议纠纷",
                "ajxz": "2",
                "spcx": "3",
                "spcxdz": "2",
                "baspt": "06        ",
                "larq": "2018-01-10T16:00",
                "jarq": "2018-04-10T06:27:09.000+0000"
            }
        ]
    }
    # jsonData = json.load(data)
    titles = ['案号', '案件名称', '立案日期', '结案日期']
    keys = ['ah', 'ajmc', 'larq', 'jarq']
    # print(data['object'])
    pageView = PageView(data['object'], titles, keys)
    pageView.renderData()
    # # pageView.renderTable()
    pageView.show()
    sys.exit(app.exec_())

