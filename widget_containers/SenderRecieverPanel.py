# SenderRecieverPanel manages the main Go-Back-N simulation display
# Coordinates multiple sender-receiver pairs and implements protocol logic

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widget_containers.SenderReciever import SenderReciever
from widget_containers.Packet import Packet

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
            # Send next packet(s) in the new window
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
