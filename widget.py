# 画一下基本的框架图。
"""
4.15.
"""


import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Main(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowFlags(Qt.FramelessWindowHint)
		# self.setStyleSheet("background-image: url(:background/bg.png);")
		# bg = QPalette(self)
		# bg.setBrush(self.backgroundRole(), QBrush(QPixmap('background/bg.png')))
		# self.setPalette(bg)
		# 待改进。
		self.resize(1000, 650)
		# self.buttons()
		self.setWindowOpacity(1)
		self.setLayout(self.layouts())

	def buttons(self):
		"""
			全部的按钮组件。
		"""
		btn_exit = QPushButton(self)
		btn_exit.setIcon(QIcon('icons/exit.png'))
		btn_exit.clicked.connect(exit)
		btn_exit.setToolTip('<font color="white">退出</font>')
		btn_exit.setStyleSheet("border: 0px;")
		btn_min = QPushButton(self)
		btn_min.setIcon(QIcon('icons/min.png'))
		btn_min.setStyleSheet("border: 0px;")
		btn_min.clicked.connect(self.showMinimized)
		btn_min.setToolTip('<font color="white">最小化</font>')
		return btn_exit, btn_min

	def layouts(self):
		hbox = QHBoxLayout()
		btn = self.buttons()
		hbox.addStretch(1)
		hbox.addWidget(btn[1])
		hbox.addWidget(btn[0])
		vbox = QVBoxLayout()
		vbox.addLayout(hbox)
		vbox.addStretch(1)
		return vbox

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