from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from ui.play_and_reset_ui import Ui_w_play_and_reset

class PlayandReset(qtw.QWidget, Ui_w_play_and_reset):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.play = False # default start value should be that the animation is paused
        self.pb_play.clicked.connect(self.play_clicked)
        self.pb_reset.clicked.connect(self.reset_clicked)

    def play_clicked(self):
        if not self.play:
            self.play = True
            self.pb_play.setText("Pause")
        else:
            self.play = False
            self.pb_play.setText("Play")
    
    def reset_clicked(self):
        pass
        
    