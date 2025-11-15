# Main entry point for the Go-Back-N simulation application
# This file initializes the PySide6 application and displays the main window

import sys
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from widget_containers.MainWidget import MainWidget

# Create the main Qt application instance
app = qtw.QApplication(sys.argv)

# Create and display the main window containing the Go-Back-N simulation
window = MainWidget()
window.show()

# Start the application event loop and exit when closed
sys.exit(app.exec())