from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from ui.sender_reciever_ui import Ui_w_sender_reciever
from widget_containers.Packet import Packet

class SenderReciever(qtw.QWidget, Ui_w_sender_reciever):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.isActive = True # boolean that will determine if this packet is ready to be sent

        self.pb_sender.clicked.connect(self.sender_clicked)
    

    def send_packet(self, prop_delay:int):
        if self.isActive:
            prop_delay = prop_delay *.1 # get proper propagation delay
            # create a packet and set the container to self
            pkt = Packet(parent = self)
            # Get coordinates for where packet should start and end for animation
            start = self.pb_sender.mapTo(self, qtc.QPoint(self.pb_sender.width(), self.pb_sender.height()//2))
            end = self.pb_reciever.mapTo(self, qtc.QPoint(self.pb_reciever.width(), self.pb_reciever.height()//2))

            # propagation delay is in terms of seconds, setDuration function expects ms
            pkt.anim.setDuration(prop_delay*1000) # set duration of animation to the propagation delay
            pkt.anim.setEasingCurve(qtc.QEasingCurve.InOutCirc) # set a nice ease in and out animation

            pkt.move(start) # move packet to start position
            pkt.show() # show packet on screen
            pkt._raise() # raise packet above all other widgets (so it is visible

            # set start and end of animation
            pkt.anim.setStartValue(start)
            pkt.anim.setEndValue(end)
            pkt.anim.start() # start animation

    def send_ACK(self, prop_delay:int):
        if self.isActive:
            prop_delay = prop_delay *.1 # get proper propagation delay
            # create a packet and set the container to self
            pkt = Packet(parent = self)
            # Get coordinates for where packet should start and end for animation
            start = self.pb_reciever.mapTo(self, qtc.QPoint(self.pb_reciever.width(), self.pb_reciever.height()//2))
            end = self.pb_sender.mapTo(self, qtc.QPoint(self.pb_sender.width(), self.pb_sender.height()//2))

            # propagation delay is in terms of seconds, setDuration function expects ms
            pkt.anim.setDuration(prop_delay*1000) # set duration of animation to the propagation delay
            pkt.anim.setEasingCurve(qtc.QEasingCurve.InOutCirc) # set a nice ease in and out animation

            pkt.move(start) # move packet to start position
            pkt.show() # show packet on screen
            pkt._raise() # raise packet above all other widgets (so it is visible)

            # set start and end of animation
            pkt.anim.setStartValue(start)
            pkt.anim.setEndValue(end)
            pkt.anim.start() # start animation 
        

# This class will create a vertical panel of all our packets that need to be sent
class SenderRecieverPanel(qtw.QWidget):
    # initialize the number of packets to 10
    def __init__(self, num_packets=10):
        super().__init__()


        # create vertical box layout for all sender receiver components
        self.vbox = qtw.QVBoxLayout(self)
        self.items = [] # list that will hold all the SenderReciever objects
        self.setPackets(num_packets)

        # Initailize the window to have a border of yellow and not react to mouse events. We will create it in the draw_window function
        self.window = qtw.QWidget()
        self.window.setStyleSheet("border:2px solid yellow; background:transparent;")
        self.window.setAttribute(qtc.Qt.WA_TransparentForMouseEvents,True)
        self.window.hide()

    # This function will update the number of sender reciever components on the users screen
    def setPackets(self, num_packets: int):

        # If the number of packets the user wants to send decreased, remove them from the UI
        while len(self.items) > num_packets:
            item = self.items.pop() # remove last element in the list of items
            # delete that item from the UI
            item.setParent(None)
            item.deleteLater()

        # If number of packets the user wants to send increased, add them to the UI
        while len(self.items) < num_packets:
            item = SenderReciever() # create a new item
            item.pb_sender.setText("Packet #"+str(len(self.items)+1))
            # add to list and UI
            self.items.append(item)
            self.vbox.addWidget(item)

    # This will draw the window that will show which senders are ready to send
    def draw_window(self, base:int, window_size:int):
        # If there are no senders and recievers, or the window size became 0, hide the window component
        if not self.items or window_size <= 0:
            self.window.hide()
            return
        
        start = max(0, min(base, self.num_packets - window_size)) # get the start of the window
        end = min(start + window_size - 1, len(self.items) - 1) # get the end of the window

        first = self.items[start] # get the first item in the window
        last = self.items[end] # get the last item in the window

        top_left = first.mapTo(self, qtc.QPoint(0, 0)) # get the top left corner of the first item
        bottom_right = last.mapTo(self, qtc.QPoint(last.width(), last.height())) # get the bottom right corner of the last item

        # Now that I have coordinates for the rectangle, draw the window and raise it to front
        rect = qtc.QRect(top_left, bottom_right).adjusted(-2, -2, 2, 2)  # tiny padding
        self.window.setGeometry(rect)
        self.window.show()
        self.window.raise_()

    def send_packets(self, prop_delay:int, re_time:int, window_size:int):
        for item in self.items:
            item.send_packet(prop_delay)

    
