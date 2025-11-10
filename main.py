import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widget_containers.MainWidget import MainWidget


app = qtw.QApplication(sys.argv)

window = MainWidget()
window.show()

sys.exit(app.exec())