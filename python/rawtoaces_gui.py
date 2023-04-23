"""

"""
from PySide6 import QtWidgets, QtCore

import os
import subprocess

class RawtoAcesGui(QtWidgets.QMainWindow):
    def __init__(self):
        super(RawtoAcesGui, self).__init__()
        self.setWindowTitle("Convert to EXR")
        self.setGeometry(800, 200, 800, 200)

        main_window = QtWidgets.QVBoxLayout()
        main_window.setContentsMargins(20, 20, 20, 20)
        main_window.setAlignment(QtCore.Qt.AlignTop)

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
        create_exr_subfolder_label = QtWidgets.QLabel("Create ´EXR´ Subfolder:")
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
        self.wb_method.setCurrentIndex(2)
        self.wb_method.setToolTip(self.wb_method_tip())

        mat_method_label = QtWidgets.QLabel("mat_method:")
        self.mat_method = QtWidgets.QComboBox()
        self.mat_method.addItems(["0", "1", "2"])
        self.mat_method.setToolTip(self.mat_method_tip())

        self.verbose_label = QtWidgets.QLabel("Verbose:")
        self.verbose = QtWidgets.QCheckBox()

        conversion_options.addWidget(wb_method_label)
        conversion_options.addWidget(self.wb_method)
        conversion_options.addWidget(mat_method_label)
        conversion_options.addWidget(self.mat_method)
        conversion_options.addWidget(self.verbose_label)
        conversion_options.addWidget(self.verbose)

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

        main_window.addLayout(import_layout)
        main_window.addLayout(file_options)
        main_window.addLayout(conversion_options)
        main_window.addLayout(raw_conversion_options_layout)
        main_window.addLayout(buttons)

        widget = QtWidgets.QWidget()
        widget.setLayout(main_window)
        self.setCentralWidget(widget)
    
    def wb_method_tip(self):
        method_tip = "White balance factor calculation method\n"
        "0=white balance using file metadata\n" 
        "1=white balance using user specified illuminant [str]\n"
        "2=Average the whole image for white balance\n"
        "3=Average a grey box for white balance <x y w h>\n"
        "4=Use custom white balance  <r g b g>\n"
        "(default = 0)"

        return method_tip

    def mat_method_tip(self):
        method_tip = "IDT matrix calculation method\n"
        "0=Calculate matrix from camera spec sens\n"
        "1=Use file metadata color matrix\n"
        "2=Use adobe coeffs included in libraw\n"
        "(default = 0)\n"
        "(default = /usr/local/include/rawtoaces/data/camera)"

        return method_tip

    def raw_conversion_options_tip(self):
        method_tip = "Raw conversion options\n add as need followed by a space, for example (-c 0.75 -C -k 1)\n"
        "-c float                Set adjust maximum threshold (default = 0.75)\n"
        "-C <r b>                Correct chromatic aberration\n"
        "-P <file>               Fix the dead pixels listed in this file\n"
        "-K <file>               Subtract dark frame (16-bit raw PGM)\n"
        "-k <num>                Set the darkness level\n"
        "-S <num>                Set the saturation level\n"
        "-n <num>                Set threshold for wavelet denoising\n"
        "-H [0-9]                Highlight mode (0=clip, 1=unclip, 2=blend, 3+=rebuild) (default = 0)\n"
        "-t [0-7]                Flip image (0=none, 3=180, 5=90CCW, 6=90CW)\n"
        "-j                      Don't stretch or rotate raw pixels\n"
        "-W                      Don't automatically brighten the image\n"
        "-b <num>                Adjust brightness (default = 1.0)\n"
        "-q [0-3]                Set the interpolation quality\n"
        "-h                      Half-size color image (twice as fast as `-q`)\n"
        "-f                      Interpolate RGGB as four colors\n"
        "-m <num>                Apply a 3x3 median filter to R-G and B-G\n"
        "-s [0..N-1]             Select one raw image from input file\n"
        "-G                      Use green_matching() filter\n"
        "-B <x y w h>            Use cropbox"

        return method_tip

    def onImportImageClicked(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")

        if file_path:
            self.file_path.setText(file_path[0])

    def getFileData(self):
        self.file_dirname = os.path.dirname(self.file_path.text())
        self.file_basename = os.path.basename(self.file_path.text())

        return self.file_dirname, self.file_basename

    def convertComand(self):
        if self.verbose.isChecked():
            verbose = "-v"
        else:
            verbose = ""

        convert_command = "rawtoaces --mat-method {0} --wb-method {1} {2} {3} {4}".format(
            self.wb_method.currentText(), 
            self.mat_method.currentText(), 
            verbose, 
            self.raw_conversion_options.text(),
            self.file_path.text()
            )

        subprocess.run(convert_command, shell=True)

    def sequenceConvertComand(self):
        if self.verbose.isChecked():
            verbose = "-v"
        else:
            verbose = ""
            
        sequence_convert_command = "rawtoaces --mat-method {0} --wb-method {1} {2} {3}".format(
            self.wb_method.currentText(), 
            self.mat_method.currentText(), 
            verbose, 
            self.raw_conversion_options.text()
            )

        command = "for images in *{0}; do {1} $images; done".format(os.path.splitext(self.file_path.text())[1], sequence_convert_command)
        subprocess.run("cd {0} && {1}".format(self.getFileData()[0], command), shell=True)

    def createSubfolder(self):
         if self.create_exr_subfolder_extention.isChecked():
            exr_subfolder = "exr"
            exr_path = "{0}/{1}".format(self.getFileData()[0], exr_subfolder)

            if not os.path.exists(exr_path):
                os.makedirs(exr_path)
            subprocess.run("cd {0} && mv {1} {2}".format(self.getFileData()[0], "*.exr", exr_path), shell=True)

    def changeImageName(self):
        input_file = os.path.splitext(self.file_path.text())[0] + "_aces.exr"
        file_path = self.getFileData()[0]
        output_file = self.change_output_image_name.text()
        output_file_path = os.path.join(file_path, output_file)

        if self.change_output_image_name.text() != "":
            subprocess.run("cd {0} && mv {1} {2}.exr".format(file_path, input_file, output_file_path), shell=True)

    def sequenceChangeImageName(self):
        input_file = os.path.splitext(self.file_path.text())[0] + "_aces.exr"
        file_path = self.getFileData()[0]
        output_file = self.change_output_image_name.text()
        output_file_path = os.path.join(file_path, output_file)

        if self.verbose.isChecked():
            echo_rename_command = "count=1001;for i in *.exr ; do echo $i {0}.$((count++)).{1} ; done".format(output_file, "${i##*.}")
        else:
            echo_rename_command = ""

        mv_rename_command = "count=1001;for i in *.exr ; do mv $i {0}.$((count++)).{1} ; done".format(output_file, "${i##*.}")

        if self.change_output_image_name.text() != "":
            subprocess.run("cd {0} && {1} && {2}".format(file_path, echo_rename_command, mv_rename_command), shell=True)

    def onConvertClicked(self):

        if self.sequence.isChecked():
            self.sequenceConvertComand()
        if self.change_output_image_name.text() != "":
            self.sequenceChangeImageName()
        if self.create_exr_subfolder_extention.isChecked():
                self.createSubfolder()

        else:
            self.convertComand()
            if self.change_output_image_name.text() != "":
                self.changeImageName()
            if self.create_exr_subfolder_extention.isChecked():
                self.createSubfolder()

    def onCloseClicked(self, event):
        self.close()
