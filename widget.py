__author__ = 'weiy'
"""
4.15.
"""
import pickle
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from index import Index
from func import *


class Main(QWidget):
    """主窗口。"""
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        # 信息。
        self.result = {'uid': 0}
        # 歌单歌曲id。
        self.playurl = {}
        # 搜索歌曲id。
        self.ids = {}
        # 本地音乐地址。
        self.local_url = {}
        # 歌曲图片。
        self.pictures = {}
        # 歌曲列表id们。
        self.playids = {}

        self.setObjectName('Main')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle('NetEase')
        self.setWindowIcon(QIcon('icons/format.ico'))
        # 功能。
        self.function = api.WebApi()
        # 主页及其他功能。
        self.index = Index(self)
        self.current_list = SongsWindow(self)
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
        self.locale_music = QPushButton(self)
        self.select_path = QPushButton(self)
        self.play = QPushButton(self)
        self.stop = QPushButton(self)
        self.nextSong = QPushButton(self)
        self.beforeSong = QPushButton(self)
        self.pause = QPushButton(self)
        self.btn_list = QPushButton(self)
        self.add_all_song = QPushButton(self)
        self.single = QPushButton(self)
        self.cycle = QPushButton(self)
        self.loop_flags = True
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
        self.spacing4 = QFrame()
        self.songs_list = QLabel(self)
        self.song_pic = QLabel(self)
        self.time1 = QLabel(self)
        self.time2 = QLabel(self)
        self.song_name = QLabel(self)
        # 歌单内的信息。
        self.detail_pic = QLabel(self)
        self.detail_pic.hide()
        self.detail_author = QLabel(self)
        self.detail_author.hide()
        self.detail_tag = QLabel(self)
        self.detail_tag.hide()
        self.detail_name = QLabel(self)
        self.detail_name.hide()
        self.detail_description = QLabel(self)
        self.detail_description.hide()
        # 标签end.
        # -------
        # 输入框start.
        self.search_line = QLineEdit(self)
        # 输入框end.
        # -------
        # 列表框start.
        self.playlist = PlayList(self)
        # 列表框end.
        # -------
        # 表格start.
        self.table = QTableWidget(self)
        self.table.setObjectName("tablelist")
        #   表格连接信号.
        self.table.itemDoubleClicked.connect(self.add_song)
        self.table.itemDoubleClicked.connect(self.play_song)
        self.table.hide()
        # 表格end.
        # -------
        # 滚动条start。
        self.slider = QSlider(self)
        # 滚动条end.
        # -------
        # 播放功能。
        self.player = QMediaPlayer()
        # -------
        # 布局与属性设置。
        self.mainLayout = QGridLayout()
        self.topLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.centerLayout = QHBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.rightLayout1 = QHBoxLayout()
        self.rightLayout2 = QVBoxLayout()
        self.rightLayout21 = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout1 = QVBoxLayout()
        self.playLayout = QHBoxLayout()
        self.set_buttons()
        self.set_labels()
        self.set_lines()
        self.set_sliders()
        self.set_medias()
        # -------
        # 其他功能。
        self.load_login()
        self.manager = QNetworkAccessManager()
        self.setLayout(self.set_layouts())

    # 登陆部分start.
    def lwindow(self):
        """
            登陆框。
        """
        login = LoginWindow(self)
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
        try:
            self.playlist.set_list()
        except:
            pass

    def quit_login(self):
        """
            退出登陆。
        """
        self.set_labels()
        self.lbe_pic.setStyleSheet("")
        self.btn_login.setText("Unlogin")
        self.btn_login.disconnect()
        self.btn_login.clicked.connect(self.lwindow)
        self.playlist.disconnect()
        self.playlist.clear()
        shutil.rmtree('data/cookies')
        os.makedirs('.' + '/data' + '/cookies')
    # 登陆部分end.

    # 内置组件部分start.

    def set_buttons(self):
        """
            全部的按钮组件。
        """
        # 退出。
        self.btn_exit.setObjectName('exit')
        self.btn_exit.setText('×')
        self.btn_exit.clicked.connect(self.close)
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
        self.find_music.clicked.connect(self.show_index)
        # 本地音乐。
        self.locale_music.setObjectName('locale')
        self.locale_music.setIcon(QIcon('icons/music.png'))
        self.locale_music.setText("本地音乐")
        self.locale_music.clicked.connect(self.looking_music)
        self.select_path.setObjectName('selection')
        self.select_path.clicked.connect(self.set_path)
        self.select_path.setText("选择目录")
        self.select_path.hide()
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
        self.single.setObjectName('single')
        self.single.setToolTip('单曲循环')
        self.single.clicked.connect(self.set_modles)
        self.single.hide()
        self.cycle.setObjectName('cycle')
        self.cycle.setToolTip('循环播放')
        self.cycle.clicked.connect(self.set_modles)
        # 歌曲列表。
        self.btn_list.setObjectName('songslist')
        self.btn_list.clicked.connect(self.songs_lists)
        # 歌单内功能。
        self.add_all_song.setObjectName("addbutton")
        self.add_all_song.setText("播放全部")
        self.add_all_song.clicked.connect(self.add_all)
        self.add_all_song.hide()

    def set_labels(self):
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
        # 时间显示组件。
        self.time1.setObjectName("time1")
        self.time1.setText('00:00')
        self.time1.setAlignment(Qt.AlignCenter | Qt.AlignRight | Qt.AlignBottom)
        self.time2.setObjectName("time2")
        self.time2.setText('00:00')
        self.time2.setAlignment(Qt.AlignBottom)
        # 间隔装饰。
        self.spacing3.setFrameShape(QFrame.VLine)
        self.spacing3.setFrameShadow(QFrame.Plain)
        self.spacing3.setLineWidth(2)
        self.spacing4.setFrameShape(QFrame.HLine)
        self.spacing3.setFrameShadow(QFrame.Plain)
        self.spacing3.setLineWidth(2)
        # 歌曲名字。
        self.song_name.setObjectName("songname")
        self.song_name.setAlignment(Qt.AlignCenter)
        self.song_name.setText("~~~还没有歌曲呦~~~")

    def set_lines(self):
        """
            输入框。
        """
        self.search_line.setObjectName('SearchLine')
        self.search_line.setPlaceholderText('搜索音乐。')

    def set_sliders(self):
        """
            滚动组件。
        """
        self.slider.setObjectName("slider")
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.slider_media)
        self.slider.sliderReleased.connect(self.slider_setdone)
    # 内置组件备份end.

    # 歌曲部分start.

    #  框架，播放器及功能的处理。
    def set_tables(self):
        """
            表格呈现歌单详细信息。
        """
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([' ', '操作', '音乐', '歌手', '专辑', '时长'])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置列宽。
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 40)
        self.table.setColumnWidth(2, 360)
        self.table.setColumnWidth(3, 140)
        self.table.setColumnWidth(4, 140)
        self.table.setColumnWidth(5, 60)
        # 设置充满表宽。
        self.table.horizontalHeader().setStretchLastSection(True)
        # 设置表头亮度。
        self.table.horizontalHeader().setHighlightSections(False)
        # 设置每次选择为一行。
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置垂直表头不显示。
        self.table.verticalHeader().setVisible(False)

    def set_medias(self):
        """
            设置播放器。
        """
        self.player.setVolume(100)
        self.player.stateChanged.connect(self.loop)
        self.player.positionChanged.connect(self.set_time)

    def song_search(self):
        """
            搜索功能。
            name: 歌曲名称。
            id: 歌曲id。
            artists: [0][1]['name']歌曲作者可能不止一人，['img1v1Url']作者头像。
            album: ['name']专辑名称。
        """ 
        # 暂时只做一页。翻页属后续功能。
        text = self.search_line.text()
        if text:
            self.set_tables()
            self.hide_index()
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
                self.ids[str(i)] = songs[i]['id']
                self.table.setItem(i, 0, QTableWidgetItem(str(i)))

                self.table.setItem(i, 1, QTableWidgetItem(QIcon('icons/playlist.png'), ''))

                self.table.setItem(i, 2, QTableWidgetItem(songs[i]['name']))

                people = ','.join([c['name'] for c in songs[i]['artists']])
                self.table.setItem(i, 3, QTableWidgetItem(people))

                self.table.setItem(i, 4, QTableWidgetItem(songs[i]['album']['name']))

                minuties = songs[i]['duration'] // 60000
                seconds = songs[i]['duration'] // 1000 % 60
                time = QTime(0, minuties, seconds)
                self.table.setItem(i, 5, QTableWidgetItem(time.toString("mm:ss")))
        else:
            return

        # 加载图片。
        pic = QPixmap()
        pic.load('icons/search2.jpg')
        self.detail_pic.setPixmap(pic.scaled(200, 200))
        self.detail_name.setText('遨游在音乐的天空。')
        self.detail_author.setText("It's my sky!")
        self.detail_tag.setText('『Music, music』')
        self.detail_description.setText('〖Search Result〗')

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
        self.set_tables()
        self.hide_index()
        details = self.function.details_playlist(self.result[name.replace('\n', '')])
        self.table.setRowCount(details['trackCount'])
        # 加载在表格里。
        for i in range(len(details['tracks'])):
            if not details['tracks'][i]['bMusic']['name']:
                self.playurl[str(i)] = details['tracks'][i]['id']
                self.pictures[str(i)] = details['tracks'][i]['album']['blurPicUrl']
            else:
                self.playurl[details['tracks'][i]['bMusic']['name']] = details['tracks'][i]['id']
                self.pictures[details['tracks'][i]['bMusic']['name']] = details['tracks'][i]['album']['blurPicUrl']
            # 设置序号。
            self.table.setItem(i, 0, QTableWidgetItem(str(i)))

            self.table.setItem(i, 1, QTableWidgetItem(QIcon('icons/playlist.png'), ''))

            if not details['tracks'][i]['bMusic']['name']:
                self.table.setItem(i, 2, QTableWidgetItem(str(i)))
            else:
                self.table.setItem(i, 2, QTableWidgetItem(details['tracks'][i]['bMusic']['name']))

            people = ','.join([t['name'] for t in details['tracks'][i]['artists']])
            self.table.setItem(i, 3, QTableWidgetItem(people))

            self.table.setItem(i, 4, QTableWidgetItem(details['tracks'][i]['album']['name']))

            minuties = details['tracks'][i]['bMusic']['playTime'] // 60000
            seconds = details['tracks'][i]['bMusic']['playTime'] // 1000 % 60
            time = QTime(0, minuties, seconds)
            self.table.setItem(i, 5, QTableWidgetItem(time.toString("mm:ss")))
        # 加载歌单图片。
        self.manager.clearAccessCache()
        pic = self.manager.get(QNetworkRequest(QUrl(details['coverImgUrl'])))
        self.manager.finished.connect(lambda: load_pic(pic))

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
            self.detail_description.setWordWrap(True)
        except TypeError:
            self.detail_description.setText('〖〗')

    #    歌曲组件start。

    def set_song(self, name, author):
        """
            设置歌曲链接连接。
        """
        try:
            self.manager.disconnect()
        except TypeError:
            pass
        self.manager.clearAccessCache()
        try:
            self.player.setMedia(QMediaContent(QUrl(self.function.details_search(self.playids[name][author]))))
            data = self.manager.get(QNetworkRequest(QUrl(self.pictures[name])))
            self.manager.finished.connect(lambda: self.load(data))
        except KeyError:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.playids[name][author])))

    def add_song(self):
        """
            将歌曲加入到播放列表。
        """
        name = self.table.item(self.table.currentRow(), 2).text()
        author = self.table.item(self.table.currentRow(), 3).text()
        times = self.table.item(self.table.currentRow(), 5).text()
        content = author + ' - ' + name + ' - ' + times
        for i in range(self.current_list.count()):
            if self.current_list.item(i).text() == content:
                if self.current_list.currentItem().text() == content:
                    break
                else:
                    self.current_list.setCurrentRow(i)
                    self.set_song(name, author)
                    break
        else:
            self.current_list.addItem(content)
            self.current_list.setCurrentRow(self.current_list.count()-1)
            try:
                self.playids[name]
            except KeyError:
                self.playids[name] = {}
                try:
                    self.playids[name][author] = self.playurl[name]
                except KeyError:
                    self.playids[name][author] = self.ids[str(self.table.currentRow())]
            self.set_song(name, author)
        # 将列表保存到文件夹下。
        with open('data/music/' + content.replace(':', '.'), 'w') as f:
            try:
                f.write(self.pictures[name])
            except KeyError:
                pass

    def add_all(self):
        """
            将表格中所有的歌曲添加到播放列表。
        """
        for i in reversed(range(self.table.rowCount())):
            name = self.table.item(i, 2).text()
            author = self.table.item(i, 3).text()
            times = self.table.item(i, 5).text()
            content = name + ' - ' + author + ' - ' + times
            temp = [self.current_list.item(j).text() for j in range(self.current_list.count())]
            if content in temp:
                pass
            else:
                self.current_list.addItem(content)
                self.playids[name] = {}
                try:
                    self.playids[name][author] = self.playurl[name]
                except KeyError:
                    self.playids[name][author] = self.ids[str(self.table.currentRow())]
            with open('data/music/' + content.replace(':', '.'), 'w') as f:
                try:
                    f.write(self.pictures[name])
                except KeyError:
                    pass
        self.set_song(name, author)
        self.play_song()

    def play_song(self):
        """
            播放组件。
        """
        # BUG: 用isAudio判断是否为有效音频是特么的双击居然显示无效。
        try:
            self.song_name.setText(self.current_list.currentItem().text().split(' - ')[1])
            self.time2.setText(self.current_list.currentItem().text().split(' - ')[2])
            self.player.play()
            self.play.hide()
            self.pause.show()
        except AttributeError:
            return

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
        self.pause.hide()
        self.play.show()

    def next_song(self):
        """
            下一首，若到头了则播放当前。
        """
        try:
            self.manager.disconnect()
        except TypeError:
            pass
        self.manager.clearAccessCache()
        try:
            content = self.current_list.item(self.current_list.currentRow()+1).text().split(' - ')
            self.song_name.setText(content[1])
            self.time2.setText(content[2])
            self.player.setMedia(QMediaContent(QUrl(self.function.details_search(self.playids[content[1]][content[0]]))))
            data = self.manager.get(QNetworkRequest(QUrl(self.pictures[content[1]])))
            self.manager.finished.connect(lambda: self.load(data))
            self.current_list.setCurrentRow(self.current_list.currentRow()+1)
            self.player.play()
        except AttributeError:
            self.player.play()

    def before_song(self):
        """
            前一首，若到头则播放当前。
        """
        try:
            self.manager.disconnect()
        except TypeError:
            pass
        self.manager.clearAccessCache()
        try:
            content = self.current_list.item(self.current_list.currentRow()-1).text().split(' - ')
            self.song_name.setText(content[1])
            self.time2.setText(content[2])
            self.player.setMedia(QMediaContent(QUrl(self.function.details_search(self.playids[content[1]][content[0]]))))
            data = self.manager.get(QNetworkRequest(QUrl(self.pictures[content[1]])))
            self.manager.finished.connect(lambda: self.load(data))
            self.current_list.setCurrentRow(self.current_list.currentRow()-1)
            self.player.play()
        except AttributeError:
            self.player.play()

    #      本地音乐查找start.
    def looking_music(self):
        """本地音乐查找组件。"""
        p = QPixmap()
        p.load('icons/local.jpg')
        self.detail_pic.setPixmap(p.scaled(200, 200))
        self.detail_name.setText("本地音乐")
        self.detail_author.setText("You, You, You")
        self.detail_tag.setText("Your Collection Music")
        self.hide_index()
        self.select_path.show()
        self.set_tables()
        self.locale_show_on_table(os.getcwd() + r"\myMusic")

    def set_path(self):
        file_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.locale_show_on_table(file_path)

    def locale_show_on_table(self, path):
        songs_list = [i for i in os.listdir(path) if i[-3:] == 'mp3']
        print(songs_list)
        self.table.setRowCount(len(songs_list))
        for i in range(len(songs_list)):
            temp = songs_list[i][:-4]
            temp2 = temp.split(' - ')
            self.table.setItem(i, 0, QTableWidgetItem(str(i)))
            self.table.setItem(i, 1, QTableWidgetItem(QIcon('icons/playlist.png'), ''))
            try:
                self.table.setItem(i, 2, QTableWidgetItem(temp2[1]))
                self.table.setItem(i, 3, QTableWidgetItem(temp2[0]))
            except IndexError:
                self.table.setItem(i, 2, QTableWidgetItem(temp))
                self.table.setItem(i, 3, QTableWidgetItem("暂时无法获取"))
                self.playids[temp] = {}
                self.playids[temp]["暂时无法获取"] = path + '\\' + songs_list[i]
                continue
            self.table.setItem(i, 4, QTableWidgetItem("暂时无法获取"))
            self.table.setItem(i, 5, QTableWidgetItem("暂时无法获取"))

            self.playids[temp2[1]] = {}
            self.playids[temp2[1]][temp2[0]] = path + '\\' + songs_list[i]
    #     本地音乐查找end.
    #    歌曲组件end.

    #    歌曲图片，时间和滚动条的设置。
    def load(self, data):
        """用于加载选中歌曲的图片。"""
        data = data.readAll()
        p = QPixmap()
        if data:
            p.loadFromData(data)
            self.song_pic.setPixmap(p.scaled(64, 64))
        else:
            p.load('icons/nosong.png')
            self.song_pic.setPixmap(p.scaled(64, 64))

    def set_time(self):
        """
            设置当前时间。
        """
        times = self.player.position() / 1000
        minutes = times // 60
        seconds = times % 60
        time = QTime(0, minutes, seconds)
        self.time1.setText(time.toString("mm:ss"))
        try:
            alltime = float(self.current_list.item(\
                self.current_list.currentRow()).text().split(' - ')[2].replace(':', '.'))
        except (AttributeError, ValueError):
            return
        curtime = float(time.toString('mm.ss'))
        self.slider.setValue((curtime / alltime) * 100)

    def slider_media(self):
        """
            拖动滚动条时时间的改变。基于时间的变化，若无法获取到时间是不变的，且会报ValueError的错误。当然可以随便写个2:00冒充。- -。
        """
        try:
            self.player.positionChanged.disconnect()
        except TypeError:
            pass
        content = self.current_list.item(self.current_list.currentRow()).text().split(' - ')
        alltime = float(content[2].replace(':', '.'))
        trans_alltime = int(alltime) * 60 + (alltime - int(alltime)) * 100
        currentTime = trans_alltime * self.slider.value()
        minuties = currentTime / 100 // 60
        seconds = currentTime / 100 % 60
        time = QTime(0, minuties, seconds)
        self.time1.setText(time.toString("mm:ss"))

    def slider_setdone(self):
        """
            鼠标放开后播放位置。待改进。
        """
        self.player.positionChanged.connect(self.set_time)
        content = self.current_list.item(self.current_list.currentRow()).text().split(' - ')
        alltime = float(content[2].replace(':', '.'))
        trans_alltime = int(alltime) * 60 + (alltime - int(alltime)) * 100
        currentTime = trans_alltime * self.slider.value()
        self.player.setPosition(currentTime * 10)

    #    设置歌曲播放模式。
    def set_modles(self):
        """
            切换图标及将循环标志变false。
        """
        if self.loop_flags:
            self.cycle.hide()
            self.single.show()
            self.loop_flags = False
        else:
            self.single.hide()
            self.cycle.show()
            self.loop_flags = True

    def loop(self):
        """
            设置为循环播放。默认。
        """
        if self.player.position() > 0 and self.player.state() == 0 and self.loop_flags:
            try:
                self.manager.disconnect()
            except TypeError:
                pass
            self.manager.clearAccessCache()
            content = self.current_list.item(self.current_list.currentRow()+1).text().split(' - ')
            self.current_list.setCurrentRow(self.current_list.currentRow()+1)
            try:
                self.player.setMedia(\
                    QMediaContent(QUrl(self.function.details_search(self.playids[content[1]][content[0]]))))
                data = self.manager.get(QNetworkRequest(QUrl(self.pictures[content[1]])))
                self.manager.finished.connect(lambda: self.load(data))
            except KeyError:
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.playids[content[1]][content[0]])))

            self.play_song()
        elif self.player.state() == 0:
            self.solo()

    def solo(self):
        """
            设置为单曲。
        """
        self.player.setPosition(0)
        self.play_song()
    # 歌曲部分end.
    # -------
    # 切换页面start。

    def songs_lists(self):
        """
            歌曲列表。
        """
        if self.current_list.flag:
            self.current_list.show()
            self.current_list.flag = False
        else:
            self.current_list.hide()
            self.current_list.flag = True

    def hide_index(self):
        """
            隐藏主页, 显示歌单详细信息。
        """
        self.centerLayout.setStretch(0, 160)
        self.centerLayout.setStretch(1, 1)
        self.centerLayout.setStretch(2, 850)
        self.centerLayout.setStretch(3, 0)
        self.centerLayout.setStretch(4, 0)
        self.index.hide()
        self.select_path.hide()
        self.current_list.hide()
        self.detail_pic.show()
        self.detail_name.show()
        self.detail_author.show()
        self.add_all_song.show()
        self.detail_tag.show()
        self.detail_description.show()
        self.table.show()

    def show_index(self):
        """
            显示主页。
        """
        self.centerLayout.setStretch(0, 160)
        self.centerLayout.setStretch(1, 1)
        self.centerLayout.setStretch(2, 0)
        self.centerLayout.setStretch(3, 850)
        self.centerLayout.setStretch(4, 0)
        self.current_list.hide()
        self.detail_pic.hide()
        self.detail_name.hide()
        self.select_path.hide()
        self.detail_author.hide()
        self.add_all_song.hide()
        self.detail_tag.hide()
        self.detail_description.hide()
        self.table.hide()
        self.index.show()
    # 切换页面end.

    # 设置布局。
    def set_layouts(self):
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
        self.leftLayout.addWidget(self.locale_music)
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
        self.rightLayout21.addWidget(self.detail_name)
        self.rightLayout21.addWidget(self.select_path)
        self.rightLayout21.addStretch(1)
        self.rightLayout2.addLayout(self.rightLayout21)
        self.rightLayout2.addWidget(self.detail_author)
        self.playLayout.addWidget(self.add_all_song)
        self.playLayout.addStretch(1)
        self.rightLayout2.addLayout(self.playLayout)
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
        self.centerLayout.addWidget(self.index)
        self.centerLayout.addWidget(self.current_list)
        self.centerLayout.setStretch(0, 180)
        self.centerLayout.setStretch(1, 1)
        self.centerLayout.setStretch(2, 0)
        self.centerLayout.setStretch(3, 830)
        self.centerLayout.setStretch(4, 0)
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
        self.bottomLayout1.addWidget(self.song_name)
        self.bottomLayout1.addWidget(self.slider)
        self.bottomLayout.addLayout(self.bottomLayout1)
        self.bottomLayout.addWidget(self.time2)
        self.bottomLayout.addWidget(self.cycle)
        self.bottomLayout.addWidget(self.single)
        self.bottomLayout.addWidget(self.btn_list)
        self.bottomLayout.setStretch(6, 1)
        self.bottomLayout.setStretch(7, 6)
        self.bottomLayout.setStretch(8, 1)
        self.mainLayout.addWidget(self.spacing4, 3, 0, Qt.AlignTop)
        self.mainLayout.addLayout(self.bottomLayout, 3, 0, Qt.AlignBottom)
        # self.mainLayout.addWidget(self.current_list, 2, 0, Qt.AlignBottom | Qt.AlignRight)
        # 下部分end.
        self.mainLayout.setRowStretch(1, 1)
        self.mainLayout.setRowStretch(2, 20)
        self.mainLayout.setRowStretch(3, 3)
        return self.mainLayout

    """重写鼠标事件，实现窗口拖动。"""
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos()-self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() and Qt.LeftButton:
                self.move(event.globalPos()-self.m_DragPosition)
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
        self.m_drag = False

    """按键绑定。。"""
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Enter-1:
            self.song_search()

    """退出窗口时做的一些事。"""
    def closeEvent(self, event):
        # 退出时保存歌曲列表缓存。
        try:
            with open('data/music/load/playids.pkl', 'wb') as f:
                pickle.dump(self.playids, f)
        except FileNotFoundError:
            pass

    """界面开始前的一些事。"""
    def showEvent(self, event):
        # 查看是否有歌曲缓存。
        try:
            with open('data/music/load/playids.pkl', 'rb') as r:
                self.playids = pickle.load(r)
        # 没有就算了。
        except FileNotFoundError:
            pass
        # 没有也不会报错。
        for i in os.listdir('.' + '/data/music/'):
            if os.path.isfile('.' + '/data/music/' + i):
                self.current_list.addItem(i.replace('.', ':'))
                with open('.' + '/data/music/' + i, 'r') as f:
                    self.pictures[i.split(' - ')[1]] = f.read()
        # 有的话设置为0，防止其他功能报错。
        self.current_list.setCurrentRow(0)