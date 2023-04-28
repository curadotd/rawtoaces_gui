"""
@package main
@brief This module contains the main function to run the GUI.

@author Marco Curado
@email mjbacurado@gmail.com
"""

from PySide6.QtWidgets import QApplication
from rawtoaces_gui import RawtoAcesGui

import sys


#Here we create the app and the window
app = QApplication(sys.argv)

#Here we create the window
window = RawtoAcesGui()
window.show()

#Here we run the app
app.exec()