# SettingsWindow provides user interface controls for Go-Back-N protocol parameters
# Allows adjustment of timing, window size, packet count, and loss simulation

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from ui.settings_window_ui import Ui_w_settings

class SettingsWindow(qtw.QWidget, Ui_w_settings):
    """Settings panel for configuring Go-Back-N simulation parameters"""
    
    # Define signals at class level - emitted when user changes settings
    changed_prop = qtc.Signal(int)          # Propagation delay changed
    changed_re_timer = qtc.Signal(int)      # Retransmission timer changed
    changed_per_pkt_loss = qtc.Signal(int)  # Packet loss percentage changed
    changed_window_size = qtc.Signal(int)   # Sender window size changed
    changed_num_packets = qtc.Signal(int)   # Total packet count changed
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Load UI from .ui file
        
        # Connect slider value changes to update functions
        self.sl_prop_delay.valueChanged.connect(self.update_prop_delay)
        self.sl_re_timer.valueChanged.connect(self.update_re_timer)
        self.sl_pkt_loss_per.valueChanged.connect(self.update_pkt_loss_per)

        # Configure propagation delay slider (controls animation speed)
        # propagation delay can range from .5 to 2 seconds. multiply cur by .1 to get correct value
        # propagation delay is the slider for animation speed for the sim essentially
        self.sl_prop_delay.setTickInterval(1)
        self.sl_prop_delay.setValue(20) # initial propagation delay will be 1 second
        self.sl_prop_delay.setRange(20, 50)  # Range: 2.0s to 5.0s

        # Configure retransmission timer slider (Go-Back-N timeout period)
        # retransmission timer will range from 3-10 seconds. Multiply cur by .1 to get correct value
        self.sl_re_timer.setTickInterval(1)
        self.sl_re_timer.setValue(50) # initial retransmission timer will be set to 5 seconds
        self.sl_re_timer.setRange(50, 100)  # Range: 5.0s to 10.0s

        # Configure packet loss simulation slider
        self.sl_pkt_loss_per.setValue(0)  # Start with no packet loss

        # Configure Go-Back-N protocol parameters
        self.spin_R.setValue(3)   # Initial window size (R)
        self.spin_K.setValue(10)  # Initial total packets (K)

        # Set valid ranges for protocol parameters
        self.spin_K.setRange(1, 20) # allow user to have a maximum of 20 packets minimum of 1
        self.spin_R.setRange(1, 10) # initialize the max window range to the initial K value

        # Connect spinbox changes to validation and signal emission
        self.spin_K.valueChanged.connect(self.update_spin_R_max)  # Ensure R <= K
        self.spin_K.valueChanged.connect(lambda: self.changed_num_packets.emit(self.spin_K.value()))
        self.spin_R.valueChanged.connect(lambda: self.changed_window_size.emit(self.spin_R.value()))

    # Slider update functions - convert slider values to display format and emit signals
    
    def update_prop_delay(self):
        """Update propagation delay display and adjust retransmission timer constraints"""
        seconds = self.sl_prop_delay.value()*.1  # Convert slider value to seconds
        self.lbl_prop_delay.setText(f"{seconds:.1f}s")
        # Ensure retransmission timer is always greater than propagation delay
        self.sl_re_timer.setRange((self.sl_prop_delay.value()*2)+10, (self.sl_prop_delay.value()*2)+80)
        if (self.sl_re_timer.value() - self.sl_prop_delay.value() <= 30):
            self.sl_re_timer.setValue((self.sl_prop_delay.value()*2)+10)
        self.changed_prop.emit(self.sl_prop_delay.value())
        
    def update_re_timer(self):
        """Update retransmission timer display and emit change signal"""
        seconds = self.sl_re_timer.value()*.1  # Convert slider value to seconds
        self.lbl_re_timer.setText(f"{seconds:.1f}s")
        self.changed_re_timer.emit(self.sl_re_timer.value())
        
    def update_pkt_loss_per(self):
        """Update packet loss percentage display and emit change signal"""
        self.lbl_pkt_loss_per.setText(str(self.sl_pkt_loss_per.value())+"%")
        self.changed_per_pkt_loss.emit(self.sl_pkt_loss_per.value())

    def update_spin_R_max(self):
        """Validate and update window size constraints when packet count changes
        
        In Go-Back-N protocol, window size (R) cannot exceed total packets (K)
        This function enforces that constraint and updates the UI accordingly
        """
        # if changing the K value makes the current R value impossible, update it
        if(self.spin_R.value() > self.spin_K.value()):
            self.spin_R.setValue(self.spin_K.value())  # Clamp R to valid range
        self.spin_R.setMaximum(self.spin_K.value()) # change window max size to the number of packets in the sim
        
