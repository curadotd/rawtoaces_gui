from PySide6.QtWidgets import QApplication
from rawtoaces_gui import RawtoAcesGui

import sys

app = QApplication(sys.argv)

window = RawtoAcesGui()
window.show()

app.exec()