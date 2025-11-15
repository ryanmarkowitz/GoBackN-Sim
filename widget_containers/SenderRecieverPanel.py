from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widget_containers.SenderReciever import SenderReciever
from widget_containers.Packet import Packet

# This class will create a vertical panel of all our packets that need to be sent
class SenderRecieverPanel(qtw.QWidget):
    # initialize the number of packets to 10
    def __init__(self, num_packets=10):
        super().__init__()


        # create vertical box layout for all sender receiver components
        self.vbox = qtw.QVBoxLayout(self)
        self.items = [] # list that will hold all the SenderReciever objects
        self.cur_ACK = 1 # index of the current ACK that is being sent
        self.base = 0 # base of the window
        self.num_packets = num_packets
        self.setPackets()
        self.windowSize = 10

        self.prop_delay = 0
        self.re_timer = 0
        self.per_pkt_loss = 0

        # Initailize the window to have a border of yellow and not react to mouse events. We will create it in the draw_window function
        self.window = qtw.QWidget(self)
        self.window.setStyleSheet("border:4px solid yellow; background:transparent;")
        self.window.setAttribute(qtc.Qt.WA_TransparentForMouseEvents,True)
        self.window.hide()
        qtc.QTimer.singleShot(30, lambda: self.draw_window(self.base))

    def changeSliders(self, prop_delay:int, re_timer:int, per_pkt_loss:int, windowSize:int, num_packets:int):
        self.prop_delay = prop_delay
        self.re_timer = re_timer
        self.per_pkt_loss = per_pkt_loss
        self.windowSize = windowSize
        self.num_packets = num_packets

    # This function will update the number of sender reciever components on the users screen
    def setPackets(self):

        # Clear any active packets before removing items
        self.clear_active_packets()
        
        # If the number of packets the user wants to send decreased, remove them from the UI
        while len(self.items) > self.num_packets:
            item = self.items.pop() # remove last element in the list of items
            # mark as deleted and delete that item from the UI
            item._is_deleted = True
            item.setParent(None)
            item.deleteLater()

        # If number of packets the user wants to send increased, add them to the UI
        while len(self.items) < self.num_packets:
            item = SenderReciever() # create a new item
            item.pb_sender.setText("Packet #"+str(len(self.items)+1))
            # make sure we label the correct number receiver and sender it is
            item.sender_num = len(self.items)+1
            item.reciever_num = len(self.items)+1
            item.pkt_arr.connect(self.on_packet_arrived)
            item.ACK_arr.connect(self.on_ACK_arrived)
            # add to list and UI
            self.items.append(item)
            self.vbox.addWidget(item)

    # This will draw the window that will show which senders are ready to send
    def draw_window(self, base:int):
        # If there are no senders and recievers, or the window size became 0, hide the window component
        if not self.items or self.windowSize <= 0:
            self.window.hide()
            return
        
        self.windowSize = self.windowSize
        
        start = max(0, min(base, self.num_packets - self.windowSize)) # get the start of the window
        end = min(start + self.windowSize - 1, len(self.items) - 1) # get the end of the window

        first = self.items[start] # get the first item in the window
        last = self.items[end] # get the last item in the window

        top_left = first.mapTo(self, qtc.QPoint(0, 0)) # get the top left corner of the first item
        bottom_right = last.mapTo(self, qtc.QPoint(last.width(), last.height())) # get the bottom right corner of the last item

        # Now that I have coordinates for the rectangle, draw the window and raise it to front
        rect = qtc.QRect(top_left, bottom_right).adjusted(-2, -2, 2, 2)  # tiny padding
        self.window.setGeometry(rect)
        self.window.show()
        self.window.raise_()

    def send_packets(self):
        # save these current values
        self.prop_delay = self.prop_delay
        self.re_timer = self.re_timer
        self.per_pkt_loss = self.per_pkt_loss

        if not self.items or self.windowSize <= 0:
            return

        start = max(0, min(self.base, self.num_packets - self.windowSize)) # get the start of the sending window
        end = min(start + self.windowSize - 1, len(self.items) - 1) # get the end of the sending window

        for i in range(start, end + 1):
            # add 30ms delay between each packet sent to simulate transmission delay
            qtc.QTimer.singleShot((50 * (i % self.windowSize)), lambda i=i: self.items[i].send_packet(self.prop_delay, self.re_timer, self.per_pkt_loss))
        
                
    def on_packet_arrived(self, sender_num:int):
        # If the packet that arrived is the next ACK needed, increase ACK
        if sender_num == self.cur_ACK:
            self.cur_ACK += 1
        # either send the next ACK, or keep sending previous ACK
        self.items[sender_num-1].send_ACK(self.prop_delay, self.per_pkt_loss, self.cur_ACK)
    
    def on_ACK_arrived(self, ACK_num:int, sender_num:int):
        # If the ACK recieved is the correct next ACK, slide the window
        if ACK_num >= sender_num + 1:
            # slide window and draw it
            if sender_num > self.base:
                self.base = sender_num 
            qtc.QTimer.singleShot(30, lambda: self.draw_window(self.base))
            # turn off functionality for the sender and reciever, turn them blue to indicate they are done
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
        # Find and delete all Packet widgets that are children of this panel
        for child in self.findChildren(Packet):
            child.deleteLater()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        qtc.QTimer.singleShot(10, lambda: self.draw_window(self.base))
