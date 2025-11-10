from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

class Packet(qtw.QPushButton):
    def __init__(self):
        super().__init__()

        # allow this packet to be animated
        self.anim = qtc.QPropertyAnimation(self, b"pos")

        self.killed = False # flag to indicate if the packet has been killed
        self.clicked.connect(self.kill) # connect the kill function to the click event

        # initialize fade out logic
        self.fx_opacity = qtw.QGraphicsOpacityEffect(self)
        self.fx_opacity.setOpacity(1.0)
        self.setGraphicsEffect(self.fx_opacity)

    # fade out once the packet has reached the reciever
    def fade_out_and_delete(self):
        fade = qtc.QPropertyAnimation(self.fx_opacity, b"opacity", self) # allow for opacity animation
        fade.setStartValue(1.0) # start the animation at full opacity
        fade.setEndValue(0.0) # end with the element dissapearing
        fade.setDuration(250) # the duration of the animation is 250ms
        fade.setEasingCurve(qtc.QEasingCurve.OutQuad) # set a nice ease out animation
        # delete the packet
        fade.finished.connect(self.deleteLater)
        fade.start()
    
    def kill(self):
        self.killed = True
        self.setStyleSheet("background-color: red;") # turn the packet red to show it has been killed
        self.fade_out_and_delete() # fade out and delete the packet