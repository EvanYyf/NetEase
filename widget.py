__author__ = 'weiy'
"""
4.15.
"""
import os
import sys
import api
import shutil
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class Main(QWidget):
    """主窗口。"""
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        # 信息。
        self.result = {'uid': 0}
        # 歌单歌曲url。
        self.playurl = {}
        # 搜索歌曲id。
        self.ids = {}
        # 歌曲图片。
        self.pictures = {}
        self.setObjectName('Main')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('NetEase')
        self.setWindowIcon(QIcon('icons/format.ico'))
        # 功能。
        self.function = api.WebApi()
        # -------
        # 待改进。
        self.resize(1000, 650)
        # 按钮start.
        self.btn_exit = QPushButton(self)
        self.btn_min = QPushButton(self)
        self.btn_max = QPushButton(self)
        self.btn_login = QPushButton("Unlogin", self)
        self.btn_search = QPushButton(self)
        self.find_music = QPushButton(self)
        self.play = QPushButton(self)
        self.stop = QPushButton(self)
        self.nextSong = QPushButton(self)
        self.beforeSong = QPushButton(self)
        self.pause = QPushButton(self)
        # 按钮end.
        # -------
        # 标签start.
        self.lbe_pic = QLabel(self)
        self.header_hr = QLabel(self)
        self.header_icon = QLabel(self)
        self.header_text = QLabel(self)
        self.spacing = QLabel(self)
        self.spacing2 = QLabel(self)
        self.spacing3 = QFrame()
        self.spacing3.setFrameShape(QFrame.VLine)
        self.spacing3.setFrameShadow(QFrame.Plain)
        self.songs_list = QLabel(self)
        self.song_pic = QLabel(self)
        # 歌单内的信息。
        self.detail_pic = QLabel(self)
        self.detail_author = QLabel(self)
        self.detail_tag = QLabel(self)
        self.detail_name = QLabel(self)
        self.detail_description = QLabel(self)
        # 标签end.
        # -------
        # 输入框start.
        self.search_line = QLineEdit(self)
        # 输入框end.
        # -------
        # 列表框start.
        self.playlist = QListWidget(self)
        # 列表框end.
        # -------
        # 表格start.
        self.table = QTableWidget(self)
        self.table.setObjectName("tablelist")
        self.table.hide()
        # 表格end.
        # -------
        # 滚动条start。
        self.slider = QSlider()
        # 滚动条end.
        # -------
        # 时间组件start。
        self.time1 = QLCDNumber()
        self.time2 = QLCDNumber()
        # 时间组件end.
        # -------
        # 布局与属性设置。
        self.mainLayout = QGridLayout()
        self.topLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.centerLayout = QHBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.rightLayout1 = QHBoxLayout()
        self.rightLayout2 = QVBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.buttons()
        self.labels()
        self.lines()
        self.sliders()
        # -------
        # 播放功能。
        self.player = QMediaPlayer()
        self.player.setVolume(100)
        # -------
        # 其他功能。
        self.load_login()
        self.manager = QNetworkAccessManager()
        self.setLayout(self.layouts())

    def lwindow(self):
        """
            登陆框。
        """
        login = LoginWindow()
        login.exec_()

    def load_login(self):
        """
            查看是否已经登陆。
        """
        os.chdir('.' + '/data' + '/cookies')
        filedir = os.listdir('.')
        if filedir:
            try:
                with open(filedir[0], 'r') as f:
                    content = f.readlines()
                    self.result['uid'] = content[1][:-1]
                    # 读入当前用户uid.
                    self.btn_login.setText(content[0][:-1])
                    # 加载昵称。
                    self.btn_login.disconnect()
                    self.btn_login.clicked.connect(self.quit_login)
                    # 改变登陆按钮连接到退出功能。
                    with open(filedir[-1], 'rb') as fi:
                        p3 = QPixmap()
                        p3.loadFromData(QByteArray(fi.read()))
                        self.lbe_pic.setStyleSheet("border: 0px;")
                        # 发现圆角只是边框，图片并不变化。
                        self.lbe_pic.setPixmap(p3.scaled(40, 40))
                    # 加载头像。
                self.btn_login.setToolTip("登出")
            except:
                pass
        else:
            pass
        os.chdir('..')
        os.chdir('..')
        self.play_lists()

    def quit_login(self):
        """
            退出登陆。
        """
        self.labels()
        self.lbe_pic.setStyleSheet("")
        self.btn_login.setText("Unlogin")
        self.btn_login.disconnect()
        self.btn_login.clicked.connect(self.lwindow)
        self.playlist.disconnect()
        self.playlist.clear()
        shutil.rmtree('data/cookies')
        os.makedirs('.' + '/data' + '/cookies')

    def buttons(self):
        """
            全部的按钮组件。
        """
        # 退出。
        self.btn_exit.setObjectName('exit')
        self.btn_exit.setText('×')
        self.btn_exit.clicked.connect(exit)
        self.btn_exit.setToolTip('退出')
        # 最小化。
        self.btn_min.setObjectName('mini')
        self.btn_min.setText('-')
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_min.setToolTip('最小化')
        # 最大化。
        self.btn_max.setObjectName('maxi')
        self.btn_max.setText('□')
        self.btn_max.setToolTip('^_^此功能已上火星')
        # 登陆。
        self.btn_login.setObjectName('login')
        self.btn_login.clicked.connect(self.lwindow)
        self.btn_login.setToolTip('登陆')
        # 搜索。
        self.btn_search.setObjectName('searchBtn')
        self.btn_search.resize(48, 48)
        self.btn_search.clicked.connect(self.song_search)
        # 发现音乐。
        self.find_music.setObjectName('find')
        self.find_music.setIcon(QIcon('icons/music.png'))
        self.find_music.setText("发现音乐")
        self.find_music.clicked.connect(self.index)
        # 播放页。
        self.play.setObjectName('play')
        self.play.setToolTip("播放歌曲")
        self.play.clicked.connect(self.play_song)
        self.stop.setObjectName('stop')
        self.stop.setToolTip("停止播放")
        self.stop.clicked.connect(self.stop_song)
        self.nextSong.setObjectName('next')
        self.nextSong.setToolTip("下一首歌曲")
        self.nextSong.clicked.connect(self.next_song)
        self.beforeSong.setObjectName('before')
        self.beforeSong.setToolTip("上一首歌曲")
        self.beforeSong.clicked.connect(self.before_song)
        self.pause.setObjectName("pause")
        self.pause.setToolTip("暂停播放")
        self.pause.hide()
        self.pause.clicked.connect(self.pause_song)

    def labels(self):
        """
            全部的标签组件。
        """
        p = QPixmap()
        p.load('icons/unlogin.png')
        p2 = QPixmap()
        p2.load('icons/format_2.png')
        # 头部装饰start。
        self.lbe_pic.setObjectName("headpic")
        self.lbe_pic.setPixmap(p.scaled(40, 40))
        self.header_hr.setObjectName('Headerhr')
        self.header_hr.setText("推荐")
        self.header_icon.setObjectName('HIcon')
        self.header_icon.setPixmap(p2.scaled(50, 50))
        self.header_text.setObjectName('HText')
        self.header_text.setText(" Music")
        # 头部装饰end。
        # 头部竖线装饰start。
        self.spacing.setObjectName('spacing1')
        self.spacing.resize(50, 50)
        self.spacing2.setObjectName('spacing2')
        self.spacing2.resize(50, 50)
        # 头部竖线装饰end。
        self.songs_list.setObjectName("songlist")
        self.songs_list.setText("我的音乐")
        # 歌单标签设置start。
        self.detail_pic.setObjectName("pic")
        self.detail_author.setObjectName("author")
        self.detail_tag.setObjectName("tag")
        self.detail_name.setObjectName("name")
        self.detail_description.setObjectName("description")
        # 歌单标签设置end。
        # 歌曲图片。
        self.song_pic.setObjectName("songpic")
        p3 = QPixmap()
        p3.load('icons/nosong.png')
        self.song_pic.setPixmap(p3)

    def lines(self):
        """
            输入框。
        """
        self.search_line.setObjectName('SearchLine')
        self.search_line.setPlaceholderText('搜索音乐。')

    def sliders(self):
        self.slider.setObjectName("slider")
        self.slider.setOrientation(Qt.Horizontal)

    def index(self):
        """
            主页面。
        """

    def tables(self):
        """
            表格呈现歌单详细信息。
        """
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([' ', '操作', '音乐', '歌手', '专辑'])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置列宽。
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 40)
        self.table.setColumnWidth(2, 360)
        self.table.setColumnWidth(3, 178)
        self.table.setColumnWidth(4, 170)
        # 设置充满表宽。
        self.table.horizontalHeader().setStretchLastSection(True)
        # 设置表头亮度。
        self.table.horizontalHeader().setHighlightSections(False)
        # 设置每次选择为一行。
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置垂直表头不显示。
        self.table.verticalHeader().setVisible(False)
        # 连接信号.
        self.table.itemDoubleClicked.connect(self.set_song)
        self.table.itemDoubleClicked.connect(self.play_song)

    def song_search(self):
        """
            搜索功能。
            name: 歌曲名称。
            id: 歌曲id。
            artists: [0][1]['name']歌曲作者可能不止一人，['img1v1Url']作者头像。
            album: ['name']专辑名称。
        """
        self.tables()
        self.table.show()
        # 加载图片。
        pic = QPixmap()
        pic.load('icons/search2.jpg')
        self.detail_pic.setPixmap(pic.scaled(200, 200))
        self.detail_name.setText('遨游在音乐的天空。')
        self.detail_author.setText("It's my sky!")
        self.detail_tag.setText('『Music, music』')
        self.detail_description.setText('〖Search Result〗')
        # 暂时只做一页。翻页属后续功能。
        text = self.search_line.text()
        if text:
            details = self.function.search(text)
            try:
                # 搜到没有的情况。
                songs = details['songs']
            except KeyError:
                self.table.hide()
                self.detail_description.setText('〖很抱歉，木有此歌曲〗')
                return
            songcount = details['songCount']
            if songcount > 100:
                count = 100
            else:
                count = songcount
            self.table.setRowCount(count)
            for i in range(count):
                for j in range(1, 5):
                    self.ids[str(i)] = songs[i]['id']
                    self.table.setItem(i, 0, QTableWidgetItem(str(i)))
                    if j == 1:
                        self.table.setItem(i, j, QTableWidgetItem(QIcon('icons/playlist.png'), ''))
                    elif j == 2:
                        self.table.setItem(i, j, QTableWidgetItem(songs[i]['name']))
                    elif j == 3:
                        people = ','.join([c['name'] for c in songs[i]['artists']])
                        self.table.setItem(i, j, QTableWidgetItem(people))
                    else:
                        self.table.setItem(i, j, QTableWidgetItem(songs[i]['album']['name']))
        else:
            pass

    def play_lists(self):
        """
            歌单列表。
        """
        for i in self.function.user_playlist(self.result['uid']):
            self.playlist.addItem(QListWidgetItem(QIcon('icons/Heart.png'), i['name']))
            self.result[i['name']] = i['id']
            # 对应歌单的id添加。
        self.playlist.currentItemChanged.connect(lambda: self.show_playlist(self.playlist.currentItem().text()))

    def show_playlist(self, name):
        """
            显示歌单详细信息。
            trackCount: 总数。
            name: 歌单名称。
            tags: 歌单标签。
            coverImgUrl: 歌单图片。
            creator: ['nickname'] 创建者名字。
            description: 歌单简介。
            tracks: 歌曲总列表[]
            ,['bMusic']['id']歌曲id，['name']歌曲名称
            , ['mp3Url']歌曲地址
            , ['artists'][0]['name']歌曲作者，['id']作者id
            , ['album']['name']专辑名称，['blurPicUrl']图片。
        """
        self.tables()
        self.table.show()
        details = self.function.details_playlist(self.result[name])
        self.table.setRowCount(details['trackCount'])
        # 加载在表格里。
        for i in range(len(details['tracks'])):
            for j in range(1, 5):
                self.playurl[details['tracks'][i]['bMusic']['name']] = details['tracks'][i]['mp3Url']
                self.pictures[details['tracks'][i]['bMusic']['name']] = details['tracks'][i]['album']['blurPicUrl']
                # 设置序号。
                self.table.setItem(i, 0, QTableWidgetItem(str(i)))
                if j == 1:
                    self.table.setItem(i, j, QTableWidgetItem(QIcon('icons/playlist.png'), ''))
                elif j == 2:
                    self.table.setItem(i, j, QTableWidgetItem(details['tracks'][i]['bMusic']['name']))
                elif j == 3:
                    people = ','.join([t['name'] for t in details['tracks'][i]['artists']])
                    self.table.setItem(i, j, QTableWidgetItem(people))
                elif j == 4:
                    self.table.setItem(i, j, QTableWidgetItem(details['tracks'][i]['album']['name']))
        # 加载歌单图片。
        self.manager.clearAccessCache()
        pic = self.manager.get(QNetworkRequest(QUrl(details['coverImgUrl'])))
        tmp = lambda: load_pic(pic)
        self.manager.finished.connect(tmp)

        def load_pic(picture):
            p4 = QPixmap()
            p4.loadFromData(picture.readAll())
            self.detail_pic.setPixmap(p4.scaled(200, 200))
        # 加载歌单名称,创建者,标签,简介。
        self.detail_name.setText('::======>>歌单: ' + details['name'])
        self.detail_author.setText('Creator: ' + details['creator']['nickname'])
        self.detail_tag.setText('『' + str(details['tags'])[1:-1] + '』')
        try:
            self.detail_description.setText('〖' + details['description'] + '〗')
        except TypeError:
            self.detail_description.setText('〖〗')

    def set_song(self):
        """歌单里的连接。"""
        self.manager.disconnect()
        self.manager.clearAccessCache()
        try:
            text = self.table.item(self.table.currentRow(), 2).text()
            self.player.setMedia(QMediaContent(QUrl(self.playurl[text])))
            data = self.manager.get(QNetworkRequest(QUrl(self.pictures[text])))
            self.manager.finished.connect(lambda: self.load(data))
        except KeyError:
            self.player.setMedia(QMediaContent(QUrl(self.function.details_search(self.ids[str(self.table.currentRow())]))))

    def play_song(self):
        """
            播放组件。
        """
        # BUG: 用isAudio判断是否为有效音频是特么的双击居然显示无效。
        self.player.play()
        self.play.hide()
        self.pause.show()

    def pause_song(self):
        """
            暂停组件。
        """
        self.player.pause()
        self.pause.hide()
        self.play.show()

    def stop_song(self):
        """
            停止组件。
        """
        self.player.stop()

    def next_song(self):
        """
            下一首，若到头了则播放当前。
        """
        self.manager.disconnect()
        self.manager.clearAccessCache()
        try:
            text = self.table.item(self.table.currentRow()+1, 2).text()
            self.player.setMedia(\
                QMediaContent(QUrl(self.playurl[text])))
            data = self.manager.get(QNetworkRequest(QUrl(self.pictures[text])))
            self.manager.finished.connect(lambda: self.load(data))
            self.table.setCurrentCell(self.table.currentRow()+1, 2)
            self.player.play()
        except AttributeError:
            self.player.play()

    def before_song(self):
        """
            前一首，若到头则播放当前。
        """
        self.manager.disconnect()
        self.manager.clearAccessCache()
        try:
            text = self.table.item(self.table.currentRow()-1, 2).text()
            self.player.setMedia(\
                QMediaContent(QUrl(self.playurl[text])))
            self.table.setCurrentCell(self.table.currentRow()-1, 2)
            data = self.manager.get(QNetworkRequest(QUrl(self.pictures[text])))
            self.manager.finished.connect(lambda: self.load(data))
            self.player.play()
        except AttributeError:
            self.player.play()

    def load(self, data):
        """用于加载选中歌曲的图片。"""
        p = QPixmap()
        p.loadFromData(data.readAll())
        self.song_pic.setPixmap(p.scaled(64, 64))

    def layouts(self):
        """
            布局。
        """
        # 头布局start.
        self.topLayout.setObjectName('Headerhbox')
        self.topLayout.addWidget(self.header_icon)
        self.topLayout.addWidget(self.header_text)
        self.topLayout.addWidget(self.spacing2)
        self.topLayout.addWidget(self.search_line)
        self.topLayout.addWidget(self.btn_search)
        self.topLayout.addStretch(1)
        self.topLayout.addWidget(self.lbe_pic)
        self.topLayout.addWidget(self.btn_login)
        self.topLayout.addWidget(self.spacing)
        self.topLayout.addWidget(self.btn_min)
        self.topLayout.addWidget(self.btn_max)
        self.topLayout.addWidget(self.btn_exit)
        self.topLayout.setSpacing(7)
        # -------
        self.mainLayout.addLayout(self.topLayout, 0, 0, Qt.AlignTop)
        self.mainLayout.addWidget(self.header_hr, 1, 0, Qt.AlignTop)
        # 头布局end.
        # --------
        # 中心布局start.
        #  左部分start.
        self.leftLayout.addWidget(self.find_music)
        self.leftLayout.addWidget(self.songs_list)
        self.leftLayout.addWidget(self.playlist)
        self.leftLayout.setSpacing(10)
        #  左部分end。
        # -------
        #  右部分start.
        self.rightLayout.addLayout(self.rightLayout1)
        self.rightLayout1.addWidget(self.detail_pic)
        self.rightLayout1.addLayout(self.rightLayout2)
        self.rightLayout1.setStretch(0, 1)
        self.rightLayout1.setStretch(1, 5)
        self.rightLayout2.addWidget(self.detail_name)
        self.rightLayout2.addWidget(self.detail_author)
        self.rightLayout2.addWidget(self.detail_tag)
        self.rightLayout2.addWidget(self.detail_description)
        self.rightLayout.addWidget(self.table)
        self.rightLayout.setStretch(0, 1)
        self.rightLayout.setStretch(1, 2)
        #  右部分end.
        # -------
        self.centerLayout.addLayout(self.leftLayout)
        self.centerLayout.addWidget(self.spacing3)
        self.centerLayout.addLayout(self.rightLayout)
        self.centerLayout.setStretch(0, 180)
        self.centerLayout.setStretch(1, 1)
        self.centerLayout.setStretch(2, 830)
        self.mainLayout.addLayout(self.centerLayout, 2, 0, Qt.AlignTop | Qt.AlignLeft)
        # 中心布局end.
        # -------
        # 下部分start.
        self.bottomLayout.addWidget(self.stop)
        self.bottomLayout.addWidget(self.beforeSong)
        self.bottomLayout.addWidget(self.play)
        self.bottomLayout.addWidget(self.pause)
        self.bottomLayout.addWidget(self.nextSong)
        self.bottomLayout.addWidget(self.song_pic)
        self.bottomLayout.addWidget(self.time1)
        self.bottomLayout.addWidget(self.slider)
        self.bottomLayout.addWidget(self.time2)
        # self.bottomLayout.addStretch(1)
        self.mainLayout.addLayout(self.bottomLayout, 3, 0, Qt.AlignBottom)
        # 下部分end.
        self.mainLayout.setRowStretch(1, 1)
        self.mainLayout.setRowStretch(2, 20)
        self.mainLayout.setRowStretch(3, 3)
        return self.mainLayout

    """重写鼠标事件，实现窗口拖动。"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos()-self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        try:
            if QMouseEvent.buttons() and Qt.LeftButton:
                self.move(QMouseEvent.globalPos()-self.m_DragPosition)
                QMouseEvent.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False


class LoginWindow(QDialog):

    """我来组成Login !"""
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setObjectName("Login")
        self.resize(200, 100)
        self.setWindowIcon(QIcon('icons/login.png'))
        self.setWindowTitle('Login')
        # 按钮start.
        self.btn_login = QPushButton('登陆', self)
        # 按钮end.
        # 标签start.
        self.lbe_user = QLabel('用户名:', self)
        self.lbe_password = QLabel('密码:', self)
        self.text_user = QLineEdit()
        self.text_pswd = QLineEdit()
        self.lbe_hide = QLabel(self)
        # 标签end.
        # -------
        # 头像下载。
        self.down_manager = QNetworkAccessManager()
        # -------
        # 布局与属性设置。
        self.buttons()
        self.loginframe()
        self.setLayout(self.vlay())
        # -------
        # 其他功能。

    def buttons(self):
        self.btn_login.setObjectName('logins')
        self.btn_login.clicked.connect(self.lgn)

    def loginframe(self):
        self.text_user.setPlaceholderText("邮箱地址")
        self.text_pswd.setPlaceholderText("密码")
        self.text_pswd.setEchoMode(QLineEdit.Password)

    def vlay(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.lbe_user)
        vbox.addWidget(self.text_user)
        vbox.addWidget(self.lbe_password)
        vbox.addWidget(self.text_pswd)
        vbox.addWidget(self.lbe_hide)
        vbox.addWidget(self.btn_login)
        vbox.addStretch(1)
        return vbox

    def lgn(self):
        user = self.text_user.text()
        pwd = self.text_pswd.text()
        func = api.WebApi()
        result = func.login(user, pwd)[1]
        if result['code'] == 200:
            self.saveCookies(result['account']['userName'], result['profile']['nickname'],\
                             result['profile']['userId'])  # 保存cookies.
            mainWindow.btn_login.setText(result['profile']['nickname'])   # 加载昵称。
            mainWindow.btn_login.disconnect()
            mainWindow.btn_login.clicked.connect(mainWindow.quit_login)
            tdata = self.down_manager.get(QNetworkRequest(QUrl(result['profile']['avatarUrl'])))
            self.down_manager.finished.connect(lambda: self.load_finish(tdata, result))    # 加载头像并保存。
            mainWindow.result['uid'] = result['profile']['userId']
            mainWindow.btn_login.setToolTip("登出")
            mainWindow.play_lists()  # 加载歌单。
        else:
            self.lbe_hide.setText('登陆失败，检查后重试。')

    def saveCookies(self, email, name, uid):
        try:
            os.chdir('.' + '/data' + '/cookies')
        except:
            os.mkdir('.' + '/data' + '/cookies')
            os.chdir('.' + '/data' + '/cookies')
        with open(email + '.dta', 'w') as f:
            f.write(name + '\n' + str(uid) + '\n')
        os.chdir('..')
        os.chdir('..')

    def load_finish(self, res, result):
        """
            加载头像并保存。
        """
        data = res.readAll()
        header = QFile('data/cookies/header' + result['profile']['avatarUrl'][-4:])
        header.open(QIODevice.WriteOnly)
        header.write(data)
        # 保存二进制文件。
        img = QPixmap()
        img.loadFromData(data)
        mainWindow.lbe_pic.setStyleSheet('border: 0px;')
        # 图片不是圆角。
        mainWindow.lbe_pic.setPixmap(img.scaled(40, 40))
        self.accept()


    """重写鼠标事件，实现窗口拖动。"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos()-self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        try:
            if QMouseEvent.buttons() and Qt.LeftButton:
                self.move(QMouseEvent.globalPos()-self.m_DragPosition)
                QMouseEvent.accept()
        except AttributeError:
            pass
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open('window.qss', 'r') as qss:
        app.setStyleSheet(qss.read())
    mainWindow = Main()
    mainWindow.show()
    sys.exit(app.exec_())