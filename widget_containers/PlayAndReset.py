from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from ui.play_and_reset_ui import Ui_w_play_and_reset

class PlayandReset(qtw.QWidget, Ui_w_play_and_reset):
    play_clicked = qtc.Signal()
    reset_clicked = qtc.Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.play = False # default start value should be that the animation is paused
        self.pb_play.clicked.connect(self.on_play_clicked)
        self.pb_reset.clicked.connect(self.on_reset_clicked)

    def on_play_clicked(self):
        self.play = True
        self.pb_play.setEnabled(False)
        self.play_clicked.emit()

        
    
    def on_reset_clicked(self):
        self.play = False
        self.pb_play.setEnabled(True)
        self.reset_clicked.emit()
    
    