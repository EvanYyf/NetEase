from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import * 
import os
import api


class LoginWindow(QDialog):

    """我来组成Login !"""
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.main = parent
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
            self.main.btn_login.setText(result['profile']['nickname'])   # 加载昵称。
            self.main.btn_login.disconnect()
            self.main.btn_login.clicked.connect(self.main.quit_login)
            tdata = self.down_manager.get(QNetworkRequest(QUrl(result['profile']['avatarUrl'])))
            self.down_manager.finished.connect(lambda: self.load_finish(tdata, result))    # 加载头像并保存。
            self.main.result['uid'] = result['profile']['userId']
            self.main.btn_login.setToolTip("登出")
            self.main.play_lists()  # 加载歌单。
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
        self.main.lbe_pic.setStyleSheet('border: 0px;')
        # 图片不是圆角。
        self.main.lbe_pic.setPixmap(img.scaled(40, 40))
        self.accept()

    """重写鼠标事件，实现窗口拖动。"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
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
        self.m_drag=False


class SongsWindow(QWidget):
    """我来组成歌曲列表。"""
    def __init__(self, parent=None):
        super(SongsWindow, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.flag = True
        self.main = parent
        self.content = QListWidget(self)
        self.addContent()
        self.hide()
        with open('func.qss', 'r') as q:
            self.setStyleSheet(q.read())

    def addContent(self):
        self.content.addItem('1')