from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from ui.settings_window_ui import Ui_w_settings

class SettingsWindow(qtw.QWidget, Ui_w_settings):
    # Define signals at class level
    changed_prop = qtc.Signal(int)
    changed_re_timer = qtc.Signal(int)
    changed_per_pkt_loss = qtc.Signal(int)
    changed_window_size = qtc.Signal(int)
    changed_num_packets = qtc.Signal(int)
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # if slider is changed by user, update 
        self.sl_prop_delay.valueChanged.connect(self.update_prop_delay)
        self.sl_re_timer.valueChanged.connect(self.update_re_timer)
        self.sl_pkt_loss_per.valueChanged.connect(self.update_pkt_loss_per)

        # propagation delay can range from .5 to 2 seconds. multiply cur by .1 to get correct value
        # propagation delay is the slider for animation speed for the sim essentially
        self.sl_prop_delay.setTickInterval(1)
        self.sl_prop_delay.setValue(10) # initial propagation delay will be 1 second
        self.sl_prop_delay.setRange(5, 20)

        # retransmission timer will range from 3-10 seconds. Multiply cur by .1 to get correct value
        self.sl_re_timer.setTickInterval(1)
        self.sl_re_timer.setValue(50) # initial retransmission timer will be set to 5 seconds
        self.sl_re_timer.setRange(30, 100)

        # set initial value of packet loss chance percentage to 0%
        self.sl_pkt_loss_per.setValue(0)

        # set initial values of spinboxes for R and K
        self.spin_R.setValue(3)
        self.spin_K.setValue(10)

        self.spin_K.setRange(1, 20) # allow user to have a maximum of 20 packets minimum of 1
        self.spin_R.setRange(1, 10) # initialize the max window range to the initial K value

        # connect spinboxes to their respective functions
        self.spin_K.valueChanged.connect(self.update_spin_R_max)
        self.spin_K.valueChanged.connect(lambda: self.changed_num_packets.emit(self.spin_K.value()))




    # These 3 functions will show the respective values in the labels next to the sliders
    def update_prop_delay(self):
        seconds = self.sl_prop_delay.value()*.1
        self.lbl_prop_delay.setText(f"{seconds:.1f}s")
        self.changed_prop.emit(self.sl_prop_delay.value())
    def update_re_timer(self):
        seconds = self.sl_re_timer.value()*.1
        self.lbl_re_timer.setText(f"{seconds:.1f}s")
        self.changed_re_timer.emit(self.sl_re_timer.value())
    def update_pkt_loss_per(self):
        self.lbl_pkt_loss_per.setText(str(self.sl_pkt_loss_per.value())+"%")
        self.changed_per_pkt_loss.emit(self.sl_pkt_loss_per.value())

    # Every time the K or number of packets for the sim is changed, we have to change the max size possible of the window
    def update_spin_R_max(self):
        # if changing the K value makes the current R value impossible, update it
        if(self.spin_R.value() > self.spin_K.value()):
            self.spin_R.setValue(self.spin_K.value())
        self.spin_R.setMaximum(self.spin_K.value()) # change window max size to the number of packets in the sim
        self.changed_window_size.emit(self.spin_R.value())
