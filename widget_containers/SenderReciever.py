from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from ui.sender_reciever_ui import Ui_w_sender_reciever
from widget_containers.Packet import Packet
import random

class SenderReciever(qtw.QWidget, Ui_w_sender_reciever):
    # Define signals at class level
    pkt_arr = qtc.Signal(int)
    ACK_arr = qtc.Signal(int,int)
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.isActive = True # boolean that will determine if this packet is ready to be sent
        self.pktLose = False # boolean that will predetermine if a packet should be lost or not
        self.ACKLose = False # boolean that will predetermine if an ACK should be lost or not
        self.sending = False # boolean that will determine if the sender is currently sending a packet
        self.ACK_ready_flag = False
        self._is_deleted = False # flag to track if object is being deleted
        
        # initialize sender and reciever numbers
        self.sender_num = 0
        self.reciever_num = 0
        self.ACKrecieved = 0 # This will keep track of what ACK the sender recieves

        # handle the sender or reciever being clicked
        self.pb_sender.clicked.connect(self.sender_clicked)
        self.pb_reciever.clicked.connect(self.reciever_clicked)
    

    def send_packet(self, prop_delay:int, re_timer:int, per_pkt_loss:int):
        if self.isActive:
            if self.sending == False:
                self.sending = True
                self.ACK_ready_flag = False # reset this flag assuming reciever never got the packet
                prop_delay = prop_delay *.1 # get proper propagation delay
                re_timer = re_timer *.1 # get proper retransmission timer
                # create a packet and set the container to parent panel
                pkt = Packet(parent = self.parent())
                # Get coordinates for where packet should start and end for animation
                start = self.pb_sender.mapTo(self.parent(), qtc.QPoint(self.pb_sender.width()//2, self.pb_sender.height()//2))
                end = self.pb_reciever.mapTo(self.parent(), qtc.QPoint(self.pb_reciever.width()//2, self.pb_reciever.height()//2))

                # propagation delay is in terms of seconds, setDuration function expects ms
                pkt.anim.setDuration(prop_delay*1000) # set duration of animation to the propagation delay
                pkt.anim.setEasingCurve(qtc.QEasingCurve.InOutCirc) # set a nice ease in and out animation

                pkt.move(start) # move packet to start position
                pkt.show() # show packet on screen
                pkt.raise_() # raise packet above all other widgets (so it is visible

                # set start and end of animation
                pkt.anim.setStartValue(start)
                pkt.anim.setEndValue(end)

                # set a timer for retransmission
                qtc.QTimer.singleShot(re_timer*1000, lambda: self.send_retransmission(pkt, prop_delay, re_timer, per_pkt_loss))

                # with a given percentage chance that a packet should be dropped, drop that packet halfway through the animation
                should_drop = (random.randint(1,100) <= per_pkt_loss) or self.pktLose # determine if the packet should be dropped
                if should_drop:
                    # Wait for half the moving animation to finish, then drop the packet
                    pkt.killed = True
                    qtc.QTimer.singleShot(prop_delay*1000/2, lambda: pkt.kill())
                    
                    qtc.QTimer.singleShot(prop_delay*1000/2, lambda: pkt.setStyleSheet("background-color: red;"))
                
                pkt.anim.start() # start animation
                pkt.anim.finished.connect(lambda: self.packet_arrived(pkt))

    def send_ACK(self, prop_delay:int, per_pkt_loss:int, ack_num:int):
        if self.isActive:
            self.sending = True
            self.ACKrecieved = ack_num
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
            # create a packet and set the container to parent panel
            pkt = Packet(parent = self.parent())
            pkt.setText("ACK #"+str(ack_num-1)) # send the correct ACK
            # Get coordinates for where packet should start and end for animation
            start = self.pb_reciever.mapTo(self.parent(), qtc.QPoint(self.pb_reciever.width()//2, self.pb_reciever.height()//2))
            end = self.pb_sender.mapTo(self.parent(), qtc.QPoint(self.pb_sender.width()//2, self.pb_sender.height()//2))

            # propagation delay is in terms of seconds, setDuration function expects ms
            pkt.anim.setDuration(prop_delay*1000) # set duration of animation to the propagation delay
            pkt.anim.setEasingCurve(qtc.QEasingCurve.InOutCirc) # set a nice ease in and out animation

            pkt.move(start) # move packet to start position
            pkt.show() # show packet on screen
            pkt.raise_() # raise packet above all other widgets (so it is visible)

            # set start and end of animation
            pkt.anim.setStartValue(start)
            pkt.anim.setEndValue(end)

            # with a given percentage chance that a packet should be dropped, drop that packet halfway through the animation
            should_drop = (random.randint(1,100) <= per_pkt_loss) # determine if the packet should be dropped
            if should_drop:
                # Wait for half the moving animation to finish, then drop the packet
                pkt.killed = True
                qtc.QTimer.singleShot(prop_delay*1000/2, lambda: pkt.fade_out_and_delete())
                qtc.QTimer.singleShot(prop_delay*1000/2, lambda: pkt.setStyleSheet("background-color: red;"))

            pkt.anim.start() # start animation
            pkt.anim.finished.connect(lambda: self.receivedACK(pkt)) 
    
    # If the sender never recieved an ACK resend the packet
    def send_retransmission(self, pkt: Packet, prop_delay:int, re_timer:int, per_pkt_loss:int):
        if self.isActive and not self._is_deleted:
            self.sending = False
            self.send_packet(prop_delay, re_timer, per_pkt_loss)
        pass
    
    # If the sender is clicked toggle whether we should predetermine the PKT being lost or not
    def sender_clicked(self):
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

    # If the reciever is clicked toggle whether we should predetermine the ACK being lost or not
    def reciever_clicked(self):
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

    def packet_arrived(self, pkt:Packet):
        if not pkt.killed and not self._is_deleted:
            self.pkt_arr.emit(self.sender_num)
            pkt.fade_out_and_delete()
    
    # If sender recieved the ACK and the ACK is the same number as the sender number, the handshake was completed
    def receivedACK(self, pkt:Packet):
        if not pkt.killed and not self._is_deleted:
            self.ACK_arr.emit(self.ACKrecieved,self.sender_num)
            pkt.fade_out_and_delete()
        

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
            self.items[i].send_packet(self.prop_delay, self.re_timer, self.per_pkt_loss)
                
    def on_packet_arrived(self, sender_num:int):
        # If the handshake hasn't finished yet, send an ACK
        if self.items[sender_num-1].isActive:
            # If the packet that arrived is the next ACK needed, increase ACK
            if sender_num == self.cur_ACK:
                self.cur_ACK += 1
            # either send the next ACK, or keep sending previous ACK
            self.items[sender_num-1].send_ACK(self.prop_delay, self.per_pkt_loss, self.cur_ACK)
    
    def on_ACK_arrived(self, ACK_num:int, sender_num:int):
        # If the ACK recieved is the correct next ACK, slide the window
        if ACK_num == sender_num + 1:
            # slide window and draw it
            self.base += 1
            qtc.QTimer.singleShot(30, lambda: self.draw_window(self.base))
            # turn off functionality for the sender and reciever, turn them blue to indicate they are done
            self.items[sender_num-1].isActive = False
            self.items[sender_num-1].pb_sender.setStyleSheet(u"QPushButton#pb_sender {\n"
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
            self.items[sender_num-1].pb_reciever.setStyleSheet(u"QPushButton#pb_reciever {\n"
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
        # If the ACK recieved is not the next ACK needed, resend the packet
        else:
            if self.cur_ACK-1 < len(self.items):
                self.items[self.cur_ACK-1].send_packet(self.prop_delay, self.re_timer, self.per_pkt_loss)
    
    def clear_active_packets(self):
        # Find and delete all Packet widgets that are children of this panel
        for child in self.findChildren(Packet):
            child.deleteLater()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        qtc.QTimer.singleShot(10, lambda: self.draw_window(self.base))
