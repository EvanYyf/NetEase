__author__ = 'weiy'

import sys
import widget
from PyQt5.QtWidgets import *


app = QApplication(sys.argv)
with open('window.qss', 'r') as qss:
    app.setStyleSheet(qss.read())
mainWindow = widget.Main()
mainWindow.show()
sys.exit(app.exec_())