from PySide6.QtWidgets import QApplication, QWidget
from convertwidget import ConvertWidget

import sys

app = QApplication(sys.argv)

window = ConvertWidget()
window.show()

app.exec()