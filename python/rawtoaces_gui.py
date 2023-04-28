"""

"""
from PySide6 import QtWidgets, QtCore, QtGui

import os
import subprocess
import re

# A regular expression, to extract the % complete.
progress_re = re.compile("Total complete: (\d+)%")

def simple_percent_parser(output):
    """
    Matches lines using the progress_re regex,
    returning a single integer for the % progress.
    """
    m = progress_re.search(output)
    if m:
        pc_complete = m.group(1)
        return int(pc_complete)


class RawtoAcesGui(QtWidgets.QMainWindow):
    def __init__(self):
        super(RawtoAcesGui, self).__init__()

        self.setWindowTitle("Raw to ACES exr")
        self.setGeometry(800, 200, 800, 200)

        main_window = QtWidgets.QVBoxLayout()
        main_window.setContentsMargins(20, 20, 20, 20)
        main_window.setAlignment(QtCore.Qt.AlignTop)

        # Create menu bar
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction("import file", self.onImportImageClicked)
        file_menu.addAction("exit", self.onCloseClicked)
        help_menu = menu.addMenu("&Help")
        help_menu.addAction("RawtoAces", self.onRawtoAcesClicked)

        #File path
        import_layout = QtWidgets.QHBoxLayout()

        file_path_label = QtWidgets.QLabel("File Path:")
        self.file_path = QtWidgets.QLineEdit()
        self.file_path.setFixedWidth(620)
        import_image = QtWidgets.QPushButton("...")
        import_image.clicked.connect(self.onImportImageClicked)

        import_layout.addWidget(file_path_label)
        import_layout.addWidget(self.file_path)
        import_layout.addWidget(import_image)
        import_layout.setAlignment(QtCore.Qt.AlignLeft)

        #File options
        file_options = QtWidgets.QHBoxLayout()
        file_options.setSpacing(4)
        file_options.setAlignment(QtCore.Qt.AlignLeft)

        sequence_label = QtWidgets.QLabel("Sequence:")
        self.sequence = QtWidgets.QCheckBox()
        create_exr_subfolder_label = QtWidgets.QLabel("Create `exr` Subfolder:")
        self.create_exr_subfolder_extention = QtWidgets.QCheckBox()
        change_output_image_name_label = QtWidgets.QLabel("Change Output Image Name:")
        self.change_output_image_name = QtWidgets.QLineEdit()
        self.change_output_image_name.setFixedWidth(200)

        file_options.addWidget(sequence_label)
        file_options.addWidget(self.sequence)
        file_options.addWidget(create_exr_subfolder_label)
        file_options.addWidget(self.create_exr_subfolder_extention)
        file_options.addWidget(change_output_image_name_label)
        file_options.addWidget(self.change_output_image_name)

        #Conversion options
        conversion_options = QtWidgets.QHBoxLayout()
        conversion_options.setSpacing(4)
        conversion_options.setAlignment(QtCore.Qt.AlignLeft)

        wb_method_label = QtWidgets.QLabel("wb_method:")
        self.wb_method = QtWidgets.QComboBox()
        self.wb_method.addItems(["0", "1", "2", "3", "4"])
        self.wb_method.setToolTip(self.wb_method_tip())

        mat_method_label = QtWidgets.QLabel("mat_method:")
        self.mat_method = QtWidgets.QComboBox()
        self.mat_method.addItems(["0", "1", "2"])
        self.mat_method.setCurrentIndex(1)
        self.mat_method.setToolTip(self.mat_method_tip())

        conversion_options.addWidget(wb_method_label)
        conversion_options.addWidget(self.wb_method)
        conversion_options.addWidget(mat_method_label)
        conversion_options.addWidget(self.mat_method)

        #Raw conversion options
        raw_conversion_options_layout = QtWidgets.QHBoxLayout()

        raw_conversion_options_label = QtWidgets.QLabel("Raw Conversion Options:")
        self.raw_conversion_options = QtWidgets.QLineEdit()

        self.raw_conversion_options.setToolTip(self.raw_conversion_options_tip())
        raw_conversion_options_layout.addWidget(raw_conversion_options_label)
        raw_conversion_options_layout.addWidget(self.raw_conversion_options)

        # Create close and export buttons
        buttons = QtWidgets.QHBoxLayout()

        convert = QtWidgets.QPushButton("Convert")
        convert.clicked.connect(self.onConvertClicked)
        close = QtWidgets.QPushButton("Close")
        close.clicked.connect(self.onCloseClicked)
        buttons.addWidget(convert)
        buttons.addWidget(close)

        buttons.setAlignment(QtCore.Qt.AlignRight)

        # Add layouts to main window
        main_window.addLayout(import_layout)
        main_window.addLayout(file_options)
        main_window.addLayout(conversion_options)
        main_window.addLayout(raw_conversion_options_layout)
        main_window.addLayout(buttons)

        widget = QtWidgets.QWidget()
        widget.setLayout(main_window)
        self.setCentralWidget(widget)
    
    def wb_method_tip(self):
        method_tip = """
        White balance factor calculation method
        0=white balance using file metadata
        1=white balance using user specified illuminant [str]
        2=Average the whole image for white balance
        3=Average a grey box for white balance <x y w h>
        4=Use custom white balance  <r g b g> 
        default = 0)
        """

        return method_tip

    def mat_method_tip(self):
        method_tip = """
        IDT matrix calculation method
        0=Calculate matrix from camera spec sens
        1=Use file metadata color matrix
        2=Use adobe coeffs included in libraw
        (default = 0)
        (default = /usr/local/include/rawtoaces/data/camera)
        """

        return method_tip

    def raw_conversion_options_tip(self):
        method_tip = """
        Raw conversion options\n add as need followed by a space, for example (-c 0.75 -C -k 1)
        -c float                Set adjust maximum threshold (default = 0.75)
        -C <r b>                Correct chromatic aberration
        -P <file>               Fix the dead pixels listed in this file
        -K <file>               Subtract dark frame (16-bit raw PGM)
        -k <num>                Set the darkness level
        -S <num>                Set the saturation level
        -n <num>                Set threshold for wavelet denoising
        -H [0-9]                Highlight mode (0=clip, 1=unclip, 2=blend, 3+=rebuild) (default = 0)
        -t [0-7]                Flip image (0=none, 3=180, 5=90CCW, 6=90CW)
        -j                      Don't stretch or rotate raw pixels
        -W                      Don't automatically brighten the image
        -b <num>                Adjust brightness (default = 1.0)
        -q [0-3]                Set the interpolation quality
        -h                      Half-size color image (twice as fast as `-q`)
        -f                      Interpolate RGGB as four colors
        -m <num>                Apply a 3x3 median filter to R-G and B-G
        -s [0..N-1]             Select one raw image from input file
        -G                      Use green_matching() filter
        -B <x y w h>            Use cropbox
        """

        return method_tip

    def onImportImageClicked(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")

        if file_path:
            self.file_path.setText(file_path[0])

    def runShellScript(self):
        if self.sequence.isChecked():
            command_to_run = self.sequenceConvertComand()
        if self.change_output_image_name.text() != "":
            command_to_run = self.sequenceChangeImageName()
        if self.create_exr_subfolder_extention.isChecked():
                command_to_run = self.createSubfolder()

        else:
            command_to_run = self.convertComand()
            if self.change_output_image_name.text() != "":
                command_to_run = self.changeImageName()
            if self.create_exr_subfolder_extention.isChecked():
                command_to_run = self.createSubfolder()

        return command_to_run

    def onCloseClicked(self, event):
        self.close()

    def onRawtoAcesClicked(self):
        rawtoaces_help = QtWidgets.QDialog(self)
        rawtoaces_help.setWindowTitle("RawtoAces Help")
        rawtoaces_help.resize(600, 600)

        layout = QtWidgets.QVBoxLayout()
        rawtoaces_help_text = self.rawToAcesHelp()
        rawtoaces_help_text_box = QtWidgets.QTextEdit()
        rawtoaces_help_text_box.setText(rawtoaces_help_text)
        rawtoaces_help_text_box.setReadOnly(True)

        layout.addWidget(rawtoaces_help_text_box)

        rawtoaces_help.setLayout(layout)
        
        rawtoaces_help.exec_()

    def rawToAcesHelp(self):
        raw_to_aces_help ="""
        rawtoaces - convert RAW digital camera files to ACES

        Usage:
          rawtoaces file ...
          rawtoaces [options] file
          rawtoaces --help
          rawtoaces --version

        IDT options:
          --help                  Show this screen
          --version               Show version
          --wb-method [0-4]       White balance factor calculation method
                                    0=white balance using file metadata 
                                    1=white balance using user specified illuminant [str] 
                                    2=Average the whole image for white balance
                                    3=Average a grey box for white balance <x y w h>
                                    4=Use custom white balance  <r g b g>
                                    (default = 0)
          --mat-method [0-2]      IDT matrix calculation method
                                    0=Calculate matrix from camera spec sens
                                    1=Use file metadata color matrix
                                    2=Use adobe coeffs included in libraw
                                    (default = 0)
                                    (default = /usr/local/include/rawtoaces/data/camera)
          --headroom float        Set highlight headroom factor (default = 6.0)
          --cameras               Show a list of supported cameras/models by LibRaw
          --valid-illums          Show a list of illuminants
          --valid-cameras         Show a list of cameras/models with available
                                  spectral sensitivity datasets

        Raw conversion options:
          -c float                Set adjust maximum threshold (default = 0.75)
          -C <r b>                Correct chromatic aberration
          -P <file>               Fix the dead pixels listed in this file
          -K <file>               Subtract dark frame (16-bit raw PGM)
          -k <num>                Set the darkness level
          -S <num>                Set the saturation level
          -n <num>                Set threshold for wavelet denoising
          -H [0-9]                Highlight mode (0=clip, 1=unclip, 2=blend, 3+=rebuild) (default = 0)
          -t [0-7]                Flip image (0=none, 3=180, 5=90CCW, 6=90CW)
          -j                      Don't stretch or rotate raw pixels
          -W                      Don't automatically brighten the image
          -b <num>                Adjust brightness (default = 1.0)
          -q [0-3]                Set the interpolation quality
          -h                      Half-size color image (twice as fast as "-q 0")
          -f                      Interpolate RGGB as four colors
          -m <num>                Apply a 3x3 median filter to R-G and B-G
          -s [0..N-1]             Select one raw image from input file
          -G                      Use green_matching() filter
          -B <x y w h>            Use cropbox

        Benchmarking options:
          -v                      Verbose: print progress messages (repeated -v will add verbosity)
          -F                      Use FILE I/O instead of streambuf API
          -d                      Detailed timing report
          -E                      Use mmap()-ed buffer instead of plain FILE I/O
        """

        return raw_to_aces_help
    
    def onConvertClicked(self):

        self.p = None

        if self.file_path.text() == "":
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a file to convert")
            return

        self.progress_window = QtWidgets.QDialog(self)
        self.progress_window.setWindowTitle("Running RawtoAces")
        self.progress_window.resize(600, 400)

        layout = QtWidgets.QVBoxLayout()
        self.text = QtWidgets.QPlainTextEdit()
        self.text.setReadOnly(True)

        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 100)

        layout.addWidget(self.progress)
        layout.addWidget(self.text)

        self.progress_window.setLayout(layout)

        self.start_process()

        self.progress_window.exec_()

    def message(self, s):
        self.text.appendPlainText(s)

    def start_process(self):
        commands = "convert.py --wb-method {0} --mat-method {1} -v {2} {3}".format(
            self.wb_method.currentText(), 
            self.mat_method.currentText(),
            self.raw_conversion_options.text(), 
            self.file_path.text())
        
        if self.create_exr_subfolder_extention.isChecked():
            commands = commands + " --create-exr-subfolder"
        if self.sequence.isChecked():
            commands = commands + " --sequence"
        if self.change_output_image_name != "":
            commands = commands + " --change-output-image-name {0}".format(self.change_output_image_name.text())

        if self.p is None:  # No process running.
            self.message("Executing process")
            self.p = QtCore.QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            self.p.start("python3", commands.split())
            

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        # Extract progress if it is in the data.
        progress = simple_percent_parser(stderr)
        if progress:
            self.progress.setValue(progress)
            self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QtCore.QProcess.NotRunning: 'Not running',
            QtCore.QProcess.Starting: 'Starting',
            QtCore.QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Process finished.")
        self.p = None
        self.progress_window.close()
