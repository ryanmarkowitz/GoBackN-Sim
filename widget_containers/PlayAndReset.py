# PlayAndReset widget provides simulation control buttons for the Go-Back-N protocol
# Contains play/pause and reset functionality for the simulation

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from ui.play_and_reset_ui import Ui_w_play_and_reset

class PlayandReset(qtw.QWidget, Ui_w_play_and_reset):
    """Control panel widget for starting/stopping and resetting the Go-Back-N simulation"""
    
    # Signals emitted when user interacts with control buttons
    play_clicked = qtc.Signal()
    reset_clicked = qtc.Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Load UI from .ui file

        self.play = False # default start value should be that the animation is paused
        # Connect button clicks to internal handlers that emit signals
        self.pb_play.clicked.connect(self.on_play_clicked)
        self.pb_reset.clicked.connect(self.on_reset_clicked)

    def on_play_clicked(self):
        """Handle play button click - starts the simulation and disables play button"""
        self.play = True
        self.pb_play.setEnabled(False)  # Disable play button during simulation
        self.play_clicked.emit()  # Notify main widget to start simulation

    def on_reset_clicked(self):
        """Handle reset button click - stops simulation and resets to initial state"""
        self.play = False
        self.pb_play.setEnabled(True)  # Re-enable play button
        self.reset_clicked.emit()  # Notify main widget to reset simulation
    
    