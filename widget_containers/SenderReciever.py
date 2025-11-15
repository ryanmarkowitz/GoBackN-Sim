# SenderReciever implements individual packet transmission pairs in Go-Back-N protocol
# Each instance represents one packet's journey from sender to receiver and back

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from ui.sender_reciever_ui import Ui_w_sender_reciever
from widget_containers.Packet import Packet
import random

class SenderReciever(qtw.QWidget, Ui_w_sender_reciever):
    """Individual sender-receiver pair for Go-Back-N packet transmission simulation"""
    
    # Define signals at class level - emitted when packets/ACKs arrive
    pkt_arr = qtc.Signal(int)      # Packet arrived at receiver (packet number)
    ACK_arr = qtc.Signal(int,int)  # ACK arrived at sender (ACK number, sender number)
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Load UI from .ui file

        # State flags for Go-Back-N protocol simulation
        self.isActive = True # boolean that will determine if this packet is ready to be sent
        self.pktLose = False # boolean that will predetermine if a packet should be lost or not
        self.ACKLose = False # boolean that will predetermine if an ACK should be lost or not
        self.sending = False # boolean that will determine if the sender is currently sending a packet
        self.ACK_ready_flag = False  # Flag indicating if receiver is ready to send ACK
        self._is_deleted = False # flag to track if object is being deleted
        
        # Packet sequence numbers for Go-Back-N protocol
        self.sender_num = 0      # Sequence number of packet being sent
        self.reciever_num = 0    # Expected sequence number at receiver
        self.ACKrecieved = 0 # This will keep track of what ACK the sender recieves

        # Connect user interaction handlers for manual packet/ACK loss simulation
        self.pb_sender.clicked.connect(self.sender_clicked)
        self.pb_reciever.clicked.connect(self.reciever_clicked)
    

    def send_packet(self, prop_delay:int, re_timer:int, per_pkt_loss:int):
        """Send a packet from sender to receiver with Go-Back-N protocol behavior
        
        Args:
            prop_delay: Propagation delay for animation (slider value * 0.1 = seconds)
            re_timer: Retransmission timer value (slider value * 0.1 = seconds) 
            per_pkt_loss: Packet loss percentage (0-100)
        """
        if self.isActive:
            if self.sending == False:
                self.sending = True
                self.ACK_ready_flag = False # reset this flag assuming reciever never got the packet
                prop_delay = prop_delay *.1 # get proper propagation delay
                re_timer = re_timer *.1 # get proper retransmission timer
                
                # Create animated packet widget with parent panel for proper layering
                pkt = Packet(parent = self.parent())
                pkt.setText(f"Packet#{self.sender_num}")
                # Calculate animation start and end positions
                start = self.pb_sender.mapTo(self.parent(), qtc.QPoint(self.pb_sender.width()//2, self.pb_sender.height()//2))
                end = self.pb_reciever.mapTo(self.parent(), qtc.QPoint(self.pb_reciever.width()//2, self.pb_reciever.height()//2))
                
                # Configure packet animation (propagation delay simulation)
                pkt.anim.setDuration(prop_delay*1000) # set duration of animation to the propagation delay
                pkt.anim.setEasingCurve(qtc.QEasingCurve.InOutCirc) # set a nice ease in and out animation

                # Position and display the packet
                pkt.move(start) # move packet to start position
                pkt.show() # show packet on screen
                pkt.raise_() # raise packet above all other widgets (so it is visible

                # Configure animation path
                pkt.anim.setStartValue(start)
                pkt.anim.setEndValue(end)

                # Set up retransmission timer (Go-Back-N timeout mechanism)
                qtc.QTimer.singleShot(re_timer*1000, lambda: self.send_retransmission(prop_delay*10, re_timer*10, per_pkt_loss))

                # Simulate packet loss based on user-defined probability or manual setting
                should_drop = (random.randint(1,100) <= per_pkt_loss) or self.pktLose # determine if the packet should be dropped
                if should_drop:
                    # Drop packet halfway through transmission (simulates network loss)
                    pkt.killed = True
                    qtc.QTimer.singleShot(prop_delay*1000/2, lambda: pkt.kill())
                    qtc.QTimer.singleShot(prop_delay*1000/2, lambda: pkt.setStyleSheet("background-color: red;"))
                    # Reset manual loss setting after packet is dropped
                    if self.pktLose:
                        qtc.QTimer.singleShot(prop_delay*1000/3, lambda: self.setSenderBack())

                # Start packet animation and connect arrival handler
                pkt.anim.start() # start animation
                pkt.anim.finished.connect(lambda: self.packet_arrived(pkt))
        


    def send_ACK(self, prop_delay:int, per_pkt_loss:int, ack_num:int):
        """Send ACK packet from receiver back to sender (Go-Back-N acknowledgment)
        
        Args:
            prop_delay: Propagation delay for animation
            per_pkt_loss: ACK loss percentage
            ack_num: Acknowledgment number being sent
        """
        self.sending = True
        self.ACKrecieved = ack_num
        
        # Update receiver appearance when sending ACK (only if not already completed)
        if ack_num == self.reciever_num+1:
            if not "background-color: blue" in self.pb_reciever.styleSheet(): # if the reciever is not blue, it means the sender is sending a duplicate ACK
                self.pb_reciever.setStyleSheet(u"QPushButton#pb_reciever {\n"
        "    background-color: lightblue;\n"
        "    border-style: outset;\n"
        "    border-width: 2px;\n"
        "    border-radius: 10px;\n"
        "    border-color: beige;\n"
        "    font: bold 14px;\n"
        "    min-width: 10em;\n"
        "    padding: 6px;\n"
        "}\n"
        "") # turn reciever light blue to show it sent an ACK
        
        prop_delay = prop_delay *.1 # get proper propagation delay
        
        # Create ACK packet with appropriate label
        pkt = Packet(parent = self.parent())
        pkt.setText("ACK #"+str(ack_num-1)) # send the correct ACK
        
        # Calculate ACK animation path (receiver to sender)
        start = self.pb_reciever.mapTo(self.parent(), qtc.QPoint(self.pb_reciever.width()//2, self.pb_reciever.height()//2))
        end = self.pb_sender.mapTo(self.parent(), qtc.QPoint(self.pb_sender.width()//2, self.pb_sender.height()//2))

        # Configure ACK animation (same timing as data packets)
        pkt.anim.setDuration(prop_delay*1000) # set duration of animation to the propagation delay
        pkt.anim.setEasingCurve(qtc.QEasingCurve.InOutCirc) # set a nice ease in and out animation

        # Position and display the ACK packet
        pkt.move(start) # move packet to start position
        pkt.show() # show packet on screen
        pkt.raise_() # raise packet above all other widgets (so it is visible)

        # Configure ACK animation path
        pkt.anim.setStartValue(start)
        pkt.anim.setEndValue(end)

        # Simulate ACK loss (ACKs can also be lost in networks)
        should_drop = (random.randint(1,100) <= per_pkt_loss) # determine if the packet should be dropped
        if should_drop or self.ACKLose:
            # Drop ACK halfway through transmission
            pkt.killed = True
            qtc.QTimer.singleShot(prop_delay*1000/2, lambda: pkt.fade_out_and_delete())
            qtc.QTimer.singleShot(prop_delay*1000/2, lambda: pkt.setStyleSheet("background-color: red;"))
            # Reset manual ACK loss setting after ACK is dropped
            if self.ACKLose:
                qtc.QTimer.singleShot(prop_delay*1000/3, lambda: self.setReceiverBack())

        # Start ACK animation and connect arrival handler
        pkt.anim.start() # start animation
        pkt.anim.finished.connect(lambda: self.receivedACK(pkt)) 
    
    def send_retransmission(self, prop_delay:int, re_timer:int, per_pkt_loss:int):
        """Handle retransmission timeout - core Go-Back-N behavior
        
        If no ACK received within timeout period, retransmit the packet
        This implements the 'Go-Back-N' timeout and retransmit mechanism
        """
        if self.isActive and not self._is_deleted:
            self.sending = False  # Reset sending state
            self.send_packet(prop_delay, re_timer, per_pkt_loss)  # Retransmit packet
    
    def sender_clicked(self):
        """Handle sender button click - toggle predetermined packet loss
        
        Allows user to manually force packet loss for demonstration purposes
        Red = packet will be lost, Green = packet will be sent normally
        """
        if self.isActive:
            # if we are currently sending or recieving a packet turn off toggle functionality
            if not self.sending:
                if not self.pktLose:
                    self.pktLose = True
                    self.pb_sender.setStyleSheet(u"QPushButton#pb_sender {\n"
"    background-color: red;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton#pb_sender:pressed {\n"
"    background-color: rgb(0, 224, 0);\n"
"    border-style: inset;\n"
"}")
                else:
                    self.pktLose = False
                    self.pb_sender.setStyleSheet(u"QPushButton#pb_sender {\n"
"    background-color: lightgreen;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton#pb_sender:pressed {\n"
"    background-color: rgb(0, 224, 0);\n"
"    border-style: inset;\n"
"}")

    def reciever_clicked(self):
        """Handle receiver button click - toggle predetermined ACK loss
        
        Allows user to manually force ACK loss for demonstration purposes
        Red = ACK will be lost, Orange = ACK will be sent normally
        """
        if self.isActive:
            # if we are currently sending or recieving a packet turn off toggle functionality
            if not self.sending:
                if not self.ACKLose:
                    self.ACKLose = True
                    self.pb_reciever.setStyleSheet(u"QPushButton#pb_reciever {\n"
"    background-color: red;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"")
                else:
                    self.ACKLose = False
                    self.pb_reciever.setStyleSheet(u"QPushButton#pb_reciever {\n"
"    background-color: orange;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"")

    def setReceiverBack(self):
        """Reset receiver to normal state after manual ACK loss"""
        self.ACKLose = False
        if not "background-color: lightblue;" in self.pb_reciever.styleSheet():
            self.pb_reciever.setStyleSheet(u"QPushButton#pb_reciever {\n"
    "    background-color: orange;\n"
    "    border-style: outset;\n"
    "    border-width: 2px;\n"
    "    border-radius: 10px;\n"
    "    border-color: beige;\n"
    "    font: bold 14px;\n"
    "    min-width: 10em;\n"
    "    padding: 6px;\n"
    "}\n"
    "")

    def setSenderBack(self):
        """Reset sender to normal state after manual packet loss"""
        self.pktLose = False
        self.pb_sender.setStyleSheet(u"QPushButton#pb_sender {\n"
"    background-color: lightgreen;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton#pb_sender:pressed {\n"
"    background-color: rgb(0, 224, 0);\n"
"    border-style: inset;\n"
"}")

    def packet_arrived(self, pkt:Packet):
        """Handle packet arrival at receiver - triggers ACK generation"""
        if not pkt.killed and not self._is_deleted:  # Only process if packet wasn't lost
            self.pkt_arr.emit(self.sender_num)  # Notify panel that packet arrived
            pkt.fade_out_and_delete()  # Clean up packet animation
    
    def receivedACK(self, pkt:Packet):
        """Handle ACK arrival at sender - completes Go-Back-N handshake
        
        If ACK matches expected sequence number, the transmission is successful
        and the window can slide forward
        """
        if not pkt.killed and not self._is_deleted:  # Only process if ACK wasn't lost
            self.ACK_arr.emit(self.ACKrecieved,self.sender_num)  # Notify panel of ACK arrival
            pkt.fade_out_and_delete()  # Clean up ACK animation
        

