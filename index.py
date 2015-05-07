from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import * 
import api


class Index(QTabWidget):
    """我是主页。"""
    def __init__(self, parent=None):
        super(Index, self).__init__(parent)
        self.main = parent
        self.pic = {}
        self.ids = {}
        # 三个主页，分别是全部歌单，新歌上架，新碟速递。
        self.index1 = QWidget()
        self.index1_area = QScrollArea()
        self.index2 = QWidget()
        self.index2_area = QTableWidget()
        self.index3 = QWidget()
        # 功能
        self.func = api.WebApi()
        # 添加页面。
        self.set_index1()
        self.set_index2()
        self.set_index3()
        self.tabs()
        # 加载样式。
        with open("index.qss", 'r') as f:
            self.setStyleSheet(f.read())

    def set_index1(self):
        """
            主页1设置。
        """
        self.index1.setObjectName("index1")
        self.index1_area.setWidget(self.index1)
        self.index1_area.setWidgetResizable(True)
        # self.index1_area.verticalScrollBar().valueChanged.connect(lambda: load_after(30))
        mainLayout = QGridLayout()

        def set_content(offer=0):
            var = locals()
            details = self.func.all_playlist(offset=offer)
            for i, j in zip(details, range(len(details))):
                self.main.result[i['name']] = i['id']
                group = QGroupBox()
                header = QLabel(self.index1)
                header.setObjectName("pictures")
                var['t' + str(j)] = Download(i['coverImgUrl'], parent=header)
                middle = QPushButton(self.index1)
                # 处理按钮的文字，使其换行。此方法不好，窗口大小重新设置的话这里也要改动。
                temp = list(i['name'])
                for c in range(len(temp)):
                    if c % 11 == 0 and c != 0:
                        temp.insert(c+1, '\n')

                middle.setText(''.join(temp))
                middle.clicked.connect(emits)
                last = QLabel(self.index1)
                if len(i['creator']['nickname']) > 18:
                    last.setText('by:' + i['creator']['nickname'][:12] + '...')
                else:
                    last.setText('by:' + i['creator']['nickname'])
                    last.setWordWrap(True)
                vbox = QVBoxLayout()
                vbox.addWidget(header)
                vbox.addWidget(middle)
                vbox.addWidget(last)
                vbox.setStretch(0, 5)
                vbox.setStretch(1, 2)
                vbox.setStretch(2, 1)
                group.setLayout(vbox)
                mainLayout.addWidget(group, (j + 0 - 0) / 5, j % 5)
            # # 多线程下载图片。
            for i in range(len(details)):
                var['t' + str(i)].start()

        def emits():
            """发送点击的数据到显示详细信息。"""
            self.main.show_playlist(self.sender().text())

        # 略卡，放弃。完善后单开个线程。
        # def load_after(offer):
        #
        #     if self.index1_area.verticalScrollBar().value() == self.index1_area.verticalScrollBar().maximum():
        #         set_content(offer=offer)
        set_content()

        self.index1.setLayout(mainLayout)

    def set_index2(self):
        """
            主页2设置。
        """
        self.index2.setObjectName("index2")

    def set_index3(self):
        """
            主页3设置。
        """
        self.index3.setObjectName("index3")

    def tabs(self):
        """
            tabwidget的一些设置等。
        """
        self.setObjectName("tabwidget")
        self.addTab(self.index1_area, "推荐")
        self.addTab(self.index2, "新歌")
        self.addTab(self.index3, "新碟")


class Download(QThread):
    """用于主页歌单等的图片加载。"""
    def __init__(self, url, parent=None):
        super(Download, self).__init__(parent)
        self.main = parent
        self.url = QUrl(url)
        self.manager = QNetworkAccessManager()

    def run(self):
        data = self.manager.get(QNetworkRequest(self.url))
        self.manager.finished.connect(lambda: self.save_pic(data))
        self.exec_()

    def save_pic(self, data):
        data = data.readAll()
        pic = QPixmap()
        pic.loadFromData(data)
        self.main.setPixmap(pic.scaled(120, 120))