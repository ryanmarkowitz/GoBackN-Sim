from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widget_containers.Packet import Packet
from widget_containers.PlayAndReset import PlayandReset
from widget_containers.SenderReciever import SenderReciever, SenderRecieverPanel
from widget_containers.SettingsWindow import SettingsWindow


class MainWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # initial starting values for settings
        self.re_timer = 50
        self.per_pkt_loss = 0
        self.prop_delay = 10
        self.window_size = 3
        self.num_packets = 10

        self.vbox = qtw.QVBoxLayout(self)
        self.settings = SettingsWindow()
        self.play_and_reset = PlayandReset()
        self.hosts_panel = SenderRecieverPanel()

        # connect the settings to the main widget's handler methods
        self.settings.changed_re_timer.connect(self.changed_re_timer)
        self.settings.changed_per_pkt_loss.connect(self.changed_per_pkt_loss)
        self.settings.changed_prop.connect(self.changed_prop_delay)
        self.settings.changed_window_size.connect(self.changed_window_size)
        self.settings.changed_num_packets.connect(self.changed_num_packets)

        self.play_and_reset.play_clicked.connect(self.play_clicked)
        self.play_and_reset.reset_clicked.connect(self.reset_clicked)

        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
        self.hosts_panel.draw_window(self.hosts_panel.base)

        self.vbox.addWidget(self.settings)
        self.vbox.addWidget(self.play_and_reset)
        self.vbox.addWidget(self.hosts_panel)
    
    # If any settings are changed, update the values in the main widget
    def changed_re_timer(self, value:int):
        self.re_timer = value
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
    def changed_per_pkt_loss(self, value:int):
        self.per_pkt_loss = value
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
    def changed_prop_delay(self, value:int):
        self.prop_delay = value
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
    def changed_window_size(self, value:int):
        self.window_size = value
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
        qtc.QTimer.singleShot(30, lambda: self.hosts_panel.draw_window(self.hosts_panel.base))
    def changed_num_packets(self, value:int):
        self.num_packets = value
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
        self.hosts_panel.setPackets()
        qtc.QTimer.singleShot(30, lambda: self.hosts_panel.draw_window(self.hosts_panel.base))
        
    def play_clicked(self):
        self.settings.setEnabled(False)
        self.hosts_panel.send_packets()
    def reset_clicked(self):
        self.settings.setEnabled(True)
        self.settings.sl_prop_delay.setValue(10)
        self.settings.sl_re_timer.setValue(50)
        self.settings.sl_pkt_loss_per.setValue(0)
        self.hosts_panel.base = 0
        self.hosts_panel.changeSliders(self.prop_delay, self.re_timer, self.per_pkt_loss, self.window_size, self.num_packets)
        self.hosts_panel.cur_ACK = 1
        self.settings.spin_K.setMinimum(0)
        qtc.QTimer.singleShot(30, lambda: self.settings.spin_K.setValue(0))
        qtc.QTimer.singleShot(30, lambda: self.settings.spin_K.setValue(10))
        qtc.QTimer.singleShot(30, lambda: self.settings.spin_R.setValue(3))
        qtc.QTimer.singleShot(30, lambda: self.hosts_panel.draw_window(self.hosts_panel.base))
        qtc.QTimer.singleShot(30, lambda: self.settings.spin_K.setMinimum(1))
        