# MainWidget serves as the central container for the Go-Back-N simulation
# Coordinates communication between settings, controls, and the simulation panel

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widget_containers.Packet import Packet
from widget_containers.PlayAndReset import PlayandReset
from widget_containers.SenderReciever import SenderReciever
from widget_containers.SenderRecieverPanel import SenderRecieverPanel
from widget_containers.SettingsWindow import SettingsWindow


class MainWidget(qtw.QWidget):
    """Main application window that orchestrates the Go-Back-N protocol simulation"""
    
    def __init__(self):
        super().__init__()

        self.setMinimumSize(900,700)

        # initial starting values for settings (Go-Back-N protocol parameters)
        self.re_timer = 50          # Retransmission timer value
        self.per_pkt_loss = 0       # Packet loss percentage
        self.prop_delay = 20        # Propagation delay for animations
        self.window_size = 3        # Sender window size (N in Go-Back-N)
        self.num_packets = 10       # Total number of packets to send

        # Create main layout and initialize all widget components
        self.vbox = qtw.QVBoxLayout(self)
        self.settings = SettingsWindow()        # Settings panel for protocol parameters
        self.play_and_reset = PlayandReset()    # Control buttons for simulation
        self.hosts_panel = SenderRecieverPanel() # Main simulation area

        # add scrollable area for better error handling if it gets too big
        self.scroll_area = qtw.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff) 
        self.scroll_area.setWidget(self.hosts_panel)

        # Connect settings changes to update handlers
        self.settings.changed_re_timer.connect(self.changed_re_timer)
        self.settings.changed_per_pkt_loss.connect(self.changed_per_pkt_loss)
        self.settings.changed_prop.connect(self.changed_prop_delay)
        self.settings.changed_window_size.connect(self.changed_window_size)
        self.settings.changed_num_packets.connect(self.changed_num_packets)

        # Connect control buttons to simulation actions
        self.play_and_reset.play_clicked.connect(self.play_clicked)
        self.play_and_reset.reset_clicked.connect(self.reset_clicked)

        # Initialize simulation panel with default values
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
        self.hosts_panel.draw_window(self.hosts_panel.base)  # Draw initial window visualization

        # Arrange widgets vertically in the main window
        self.vbox.addWidget(self.settings)
        self.vbox.addWidget(self.play_and_reset)
        self.vbox.addWidget(self.scroll_area)
    
    # Settings change handlers - update simulation parameters when user modifies settings
    
    def changed_re_timer(self, value:int):
        """Update retransmission timer value and propagate to simulation"""
        self.re_timer = value
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
        
    def changed_per_pkt_loss(self, value:int):
        """Update packet loss percentage and propagate to simulation"""
        self.per_pkt_loss = value
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
        
    def changed_prop_delay(self, value:int):
        """Update propagation delay (animation speed) and propagate to simulation"""
        self.prop_delay = value
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
        
    def changed_window_size(self, value:int):
        """Update sender window size (N in Go-Back-N) and redraw window visualization"""
        self.window_size = value
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
        # Redraw window after brief delay to ensure UI updates are complete
        qtc.QTimer.singleShot(50, lambda: self.hosts_panel.draw_window(self.hosts_panel.base))
        
    def changed_num_packets(self, value:int):
        """Update total number of packets and recreate packet UI elements"""
        self.num_packets = value
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
        self.hosts_panel.setPackets()  # Recreate packet widgets to match new count
        # Redraw window after brief delay to ensure UI updates are complete
        qtc.QTimer.singleShot(50, lambda: self.hosts_panel.draw_window(self.hosts_panel.base))
        
    def play_clicked(self):
        """Start the Go-Back-N simulation - disable settings and begin packet transmission"""
        self.settings.setEnabled(False)  # Prevent settings changes during simulation
        self.hosts_panel.send_packets()  # Begin sending packets within the current window
        
    def reset_clicked(self):
        """Reset simulation to initial state - restore default settings and clear progress"""
        self.settings.setEnabled(True)  # Re-enable settings modification
        
        # Reset all settings to default values
        self.settings.sl_prop_delay.setValue(20)
        self.settings.sl_re_timer.setRange(50, 100)
        self.settings.sl_re_timer.setValue(50)
        self.settings.sl_pkt_loss_per.setValue(0)
        
        # Reset simulation state
        self.hosts_panel.base = 0        # Reset window base position
        self.hosts_panel.cur_ACK = 1     # Reset expected ACK number
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
        
        # Reset spinbox values with proper sequencing to avoid validation issues
        self.settings.spin_K.setMinimum(0)  # Temporarily allow 0 to reset cleanly
        qtc.QTimer.singleShot(50, lambda: self.settings.spin_K.setValue(0))
        qtc.QTimer.singleShot(100, lambda: self.settings.spin_K.setValue(10))
        qtc.QTimer.singleShot(150, lambda: self.settings.spin_R.setValue(3))
        qtc.QTimer.singleShot(100, lambda: self.hosts_panel.draw_window(self.hosts_panel.base))
        qtc.QTimer.singleShot(100, lambda: self.settings.spin_K.setMinimum(1))  # Restore minimum
        