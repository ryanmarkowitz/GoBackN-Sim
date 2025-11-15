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
        

class SenderRecieverPanel(qtw.QWidget):
    """Main simulation panel managing multiple sender-receiver pairs for Go-Back-N protocol
    
    This class orchestrates the entire Go-Back-N simulation, managing:
    - Sliding window visualization
    - Packet transmission coordination
    - ACK processing and window advancement
    - Protocol state management
    """
    
    def __init__(self, num_packets=10):
        super().__init__()

        # Create layout for sender-receiver pairs
        self.vbox = qtw.QVBoxLayout(self)
        self.items = [] # list that will hold all the SenderReciever objects
        
        # Go-Back-N protocol state variables
        self.cur_ACK = 1 # index of the current ACK that is being sent
        self.base = 0 # base of the window (leftmost unacknowledged packet)
        self.num_packets = num_packets  # Total packets to transmit
        self.windowSize = 10  # Sender window size (N in Go-Back-N)
        
        # Initialize packet UI elements
        self.setPackets()
        
        # Simulation parameters (updated from settings)
        self.prop_delay = 0    # Propagation delay
        self.re_timer = 0      # Retransmission timer
        self.per_pkt_loss = 0  # Packet loss percentage

        # Create sliding window visualization overlay
        self.window = qtw.QWidget(self)
        self.window.setStyleSheet("border:4px solid yellow; background:transparent;")
        self.window.setAttribute(qtc.Qt.WA_TransparentForMouseEvents,True)  # Allow clicks through
        self.window.hide()  # Initially hidden
        # Draw initial window after brief delay to ensure UI is ready
        qtc.QTimer.singleShot(30, lambda: self.draw_window(self.base))

    def changeSliders(self, prop_delay:int, re_timer:int, per_pkt_loss:int, windowSize:int, num_packets:int):
        """Update simulation parameters from settings panel
        
        Called whenever user modifies settings to keep simulation in sync
        """
        self.prop_delay = prop_delay      # Animation speed
        self.re_timer = re_timer          # Timeout period
        self.per_pkt_loss = per_pkt_loss  # Loss probability
        self.windowSize = windowSize      # Go-Back-N window size
        self.num_packets = num_packets    # Total packet count

    def setPackets(self):
        """Dynamically adjust the number of sender-receiver pairs based on packet count
        
        Creates or removes UI elements to match the desired number of packets
        Each pair represents one packet in the Go-Back-N sequence
        """

        # Clear any active packets before removing items to prevent orphaned animations
        self.clear_active_packets()
        
        # Remove excess sender-receiver pairs if packet count decreased
        while len(self.items) > self.num_packets:
            item = self.items.pop() # remove last element in the list of items
            # Mark as deleted and clean up UI element
            item._is_deleted = True
            item.setParent(None)
            item.deleteLater()

        # Add new sender-receiver pairs if packet count increased
        while len(self.items) < self.num_packets:
            item = SenderReciever() # create a new item
            item.pb_sender.setText("Packet #"+str(len(self.items)+1))
            
            # Assign sequence numbers for Go-Back-N protocol
            item.sender_num = len(self.items)+1
            item.reciever_num = len(self.items)+1
            
            # Connect packet/ACK arrival signals to protocol handlers
            item.pkt_arr.connect(self.on_packet_arrived)
            item.ACK_arr.connect(self.on_ACK_arrived)
            
            # Add to UI and internal list
            self.items.append(item)
            self.vbox.addWidget(item)

    def draw_window(self, base:int):
        """Draw visual representation of Go-Back-N sliding window
        
        The yellow border shows which packets are currently in the sender's window
        and can be transmitted without waiting for ACKs
        
        Args:
            base: Starting position of the sliding window (leftmost unACKed packet)
        """
        # Hide window if no packets or invalid window size
        if not self.items or self.windowSize <= 0:
            self.window.hide()
            return
        
        # Calculate window boundaries (ensure within valid range)
        start = max(0, min(base, self.num_packets - self.windowSize)) # get the start of the window
        end = min(start + self.windowSize - 1, len(self.items) - 1) # get the end of the window

        # Get UI elements at window boundaries
        first = self.items[start] # get the first item in the window
        last = self.items[end] # get the last item in the window

        # Calculate window overlay position
        top_left = first.mapTo(self, qtc.QPoint(0, 0)) # get the top left corner of the first item
        bottom_right = last.mapTo(self, qtc.QPoint(last.width(), last.height())) # get the bottom right corner of the last item

        # Position and display the window overlay
        rect = qtc.QRect(top_left, bottom_right).adjusted(-2, -2, 2, 2)  # tiny padding
        self.window.setGeometry(rect)
        self.window.show()
        self.window.raise_()  # Bring to front

    def send_packets(self):
        """Send all packets within the current Go-Back-N window
        
        This implements the core Go-Back-N behavior: send up to N packets
        without waiting for ACKs, where N is the window size
        """
        # Validate simulation state
        if not self.items or self.windowSize <= 0:
            return

        # Calculate current window boundaries
        start = max(0, min(self.base, self.num_packets - self.windowSize)) # get the start of the sending window
        end = min(start + self.windowSize - 1, len(self.items) - 1) # get the end of the sending window

        # Send all packets in the current window with staggered timing
        for i in range(start, end + 1):
            # Add small delay between each packet sent to simulate transmission delay
            qtc.QTimer.singleShot((50 * (i % self.windowSize)), lambda i=i: self.items[i].send_packet(self.prop_delay, self.re_timer, self.per_pkt_loss))
        
                
    def on_packet_arrived(self, sender_num:int):
        """Handle packet arrival at receiver - implements Go-Back-N ACK logic
        
        In Go-Back-N, receiver only accepts packets in order and ACKs
        the highest in-order packet received
        
        Args:
            sender_num: Sequence number of the arrived packet
        """
        # Go-Back-N: only advance expected ACK if packet is in order
        if sender_num == self.cur_ACK:
            self.cur_ACK += 1  # Advance to next expected packet
        # Always ACK the highest in-order packet received (cumulative ACK)
        self.items[sender_num-1].send_ACK(self.prop_delay, self.per_pkt_loss, self.cur_ACK)
    
    def on_ACK_arrived(self, ACK_num:int, sender_num:int):
        """Handle ACK arrival at sender - implements Go-Back-N window sliding
        
        In Go-Back-N, ACKs are cumulative. An ACK for packet N acknowledges
        all packets up to and including N. Window slides forward accordingly.
        
        Args:
            ACK_num: Acknowledgment number received
            sender_num: Sender that received the ACK
        """
        # Check if this ACK advances the window (acknowledges packets)
        if ACK_num >= sender_num + 1:
            # Slide window forward (Go-Back-N window advancement)
            if sender_num > self.base:
                self.base = sender_num 
            qtc.QTimer.singleShot(30, lambda: self.draw_window(self.base))  # Update window visualization
            
            # Mark acknowledged sender-receiver pairs as completed
            for i in range(sender_num):
                self.items[i].isActive = False
                self.items[i].pb_sender.setStyleSheet(u"QPushButton#pb_sender {\n"
    "    background-color: blue;\n"
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
                self.items[i].pb_reciever.setStyleSheet(u"QPushButton#pb_reciever {\n"
    "    background-color: blue;\n"
    "    border-style: outset;\n"
    "    border-width: 2px;\n"
    "    border-radius: 10px;\n"
    "    border-color: beige;\n"
    "    font: bold 14px;\n"
    "    min-width: 10em;\n"
    "    padding: 6px;\n"
    "}\n"
    "")
                # after sliding the window send the next packet
                self.send_packets()
    
    def clear_active_packets(self):
        """Clean up any active packet animations before resetting simulation"""
        # Find and delete all Packet widgets that are children of this panel
        for child in self.findChildren(Packet):
            child.deleteLater()
    
    def resizeEvent(self, event):
        """Handle window resize - redraw sliding window overlay to match new layout"""
        super().resizeEvent(event)
        # Redraw window after brief delay to ensure layout is complete
        qtc.QTimer.singleShot(10, lambda: self.draw_window(self.base))
