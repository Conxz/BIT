# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from MiscDialog import MiscDialog

import os
import sys

from ssmbnu import ssmbnu
from pbmbnu import pbmbnu

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class MBNUDialog(QDialog):
    def __init__(self, parent=None):
        super(MBNUDialog, self).__init__(parent)

        self.setWindowTitle('MBNU - Morphological Brain Network Utility')
        self.setFixedSize(600, 200) #Fixed the window size
        self._temp_dir = QDir.currentPath()

        self._init_gui()
        self._create_actions()
        
        self.data_path = None
        self.seg_file = None
        self.label_file = None
        self.sessid_file = None

    def _init_gui(self):
        #Data Path
        data_path = QLabel('Data Path')
        self._data_path_dir = QLineEdit('')
        self._data_path_button = QPushButton('...')
        self._data_path_button.setFixedWidth(80)

        #Seg. File
        seg_file_path = QLabel('Seg. File')
        self._seg_path_dir = QLineEdit('')
        self._seg_path_button = QPushButton('...')
        self._seg_path_button.setFixedWidth(80)
        
        #Seg. Label File
        label_file_path = QLabel('Label File')
        self._label_path_dir = QLineEdit('')
        self._label_path_button = QPushButton('...')
        self._label_path_button.setFixedWidth(80)

        #Advanced Options
        self._advanced_options_check = QCheckBox('Advanced Options')
        self._advanced_options_check.setChecked(False)
        sessid_file_path = QLabel('SessID File')
        self._sessid_file_dir = QLineEdit('')
        self._sessid_file_dir.setReadOnly(True)
        # self._sessid_file_dir.setVisible(False)
        self._sessid_file_button = QPushButton('...')
        self._sessid_file_button.setFixedWidth(80)
        # self._sessid_file_button.setVisible(False)
        self._calculate_population_based_mbn_check = QCheckBox('Calculate population-based MBN')

        #layout the advanced options part
        advanced_hboxlayout = QHBoxLayout()
        advanced_hboxlayout.addWidget(sessid_file_path)
        advanced_hboxlayout.addWidget(self._sessid_file_dir)
        advanced_hboxlayout.addWidget(self._sessid_file_button)

        advanced_vboxlayout = QVBoxLayout()
        advanced_vboxlayout.addLayout(advanced_hboxlayout)
        advanced_vboxlayout.addWidget(self._calculate_population_based_mbn_check)

        self._advanced_groupbox = QGroupBox()
        self._advanced_groupbox.setLayout(advanced_vboxlayout)
        self._advanced_groupbox.setVisible(False)

        #Layout the data path, seg. file and advanced options part and the buttons part.
        grid_layout = QGridLayout()
        grid_layout.addWidget(data_path, 0, 0, 1, 1)
        grid_layout.addWidget(self._data_path_dir, 0, 1, 1, 3)
        grid_layout.addWidget(self._data_path_button, 0, 4, 1, 1)
        grid_layout.addWidget(seg_file_path, 1, 0, 1, 1)
        grid_layout.addWidget(self._seg_path_dir, 1, 1, 1, 3)
        grid_layout.addWidget(self._seg_path_button, 1, 4, 1, 1)
        grid_layout.addWidget(label_file_path, 2, 0, 1, 1)
        grid_layout.addWidget(self._label_path_dir, 2, 1, 1, 3)
        grid_layout.addWidget(self._label_path_button, 2, 4, 1, 1)

        grid_layout.addWidget(self._advanced_options_check, 3, 0, 1, 1)
        grid_layout.addWidget(self._advanced_groupbox, 4, 0, 1, 5)

        self._go_button = QPushButton('Go')
        self._exit_button = QPushButton('Exit')
        self._misc_button = QPushButton('Misc')
        self._go_button.setFixedWidth(120)
        self._exit_button.setFixedWidth(120)
        self._misc_button.setFixedWidth(120)

        hboxlayout = QHBoxLayout()
        hboxlayout.addWidget(self._go_button)
        hboxlayout.addWidget(self._exit_button)
        hboxlayout.addWidget(self._misc_button)

        button_groupbox = QGroupBox()
        button_groupbox.setLayout(hboxlayout)

        vboxlayout = QVBoxLayout()
        vboxlayout.addLayout(grid_layout)
        vboxlayout.addWidget(button_groupbox)

        self.setLayout(vboxlayout)
        # self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def _create_actions(self):
        self._misc_button.clicked.connect(self._open_misc_dialog)
        self._exit_button.clicked.connect(self.done)
        self._go_button.clicked.connect(self._go) # running
        self._advanced_options_check.clicked.connect(self._enable_advanced_options)
        self._calculate_population_based_mbn_check.clicked.connect(self._calculate_MBN_checked)
        self._data_path_button.clicked.connect(self._data_path_browse)
        self._seg_path_button.clicked.connect(self._seg_file_browse)
        self._label_path_button.clicked.connect(self._label_file_browse)
        self._sessid_file_button.clicked.connect(self._sessid_file_browse)

    def _enable_advanced_options(self):
        if self._advanced_options_check.isChecked():
            self._advanced_groupbox.setVisible(True)
            self.setFixedSize(600, 300)
        else:
            self._advanced_groupbox.setVisible(False)
            self._sessid_file_dir.clear()
            self._calculate_population_based_mbn_check.setChecked(False)
            self.setFixedSize(600, 200)

    def _open_misc_dialog(self):
        misc_dialog = MiscDialog(self)
        misc_dialog.exec_()

    def _go(self):
        if self.data_path == None or self.seg_file == None or self.label_file == None:
            QMessageBox.warning(self,
                                'MBNU Warning',
                                'Data Path/Seg. File/Lable File must be set!',
                                QMessageBox.Yes)
        else:
            self._go_button.setEnabled(False)
            tag = ssmbnu(self.data_path, self.seg_file, self.label_file, self.sessid_file)
            if self._calculate_population_based_mbn_check.isChecked():
                tag0 = pbmbnu(self.data_path, self.seg_file, self.label_file, self.sessid_file)
                if tag == 1 and tag0 ==1:
                    print "Finished!"
            else:
                if tag == 1:
                    print "Finished!"
                    #self._go_button.setEnabled(True)

    #Open file dialog
    def _open_file_dialog(self, title):
        file_name = QFileDialog.getOpenFileName(self,
                                                title,
                                                self._temp_dir,
                                                "Seg files(*.*)")
        file_path = None
        if not file_name.isEmpty():
            if sys.platform == 'win32':
                file_path = unicode(file_name).encode('gb2312')
            else:
                file_path = str(file_name)
        return file_path

    #Get exist derectory
    def _open_folder_dialog(self, title):
        file_name = QFileDialog.getExistingDirectory(self,
                                                    title,
                                                    self._temp_dir)
        import sys
        file_path = None
        if not file_name.isEmpty():
            if sys.platform == 'win32':
                file_path = unicode(file_name).encode('gb2312')
            else:
                file_path = str(file_name)
        return file_path

    def _data_path_browse(self):
        data_path = self._open_folder_dialog("Data Path folder select")

        if data_path:
            self._data_path_dir.setText(data_path)
            self.data_path = data_path
            print 'Data Path: ', data_path
        else:
            print 'Nothing has been selected!'

    def _seg_file_browse(self):
        seg_file = self._open_file_dialog("Seg. File")

        if seg_file:
            self._seg_path_dir.setText(seg_file)
            self.seg_file = seg_file
            print 'Seg. File: ', seg_file
        else:
            print 'Nothing has been selected!'
    
    def _label_file_browse(self):
        label_file = self._open_file_dialog("Label File")

        if label_file:
            self._label_path_dir.setText(label_file)
            self.label_file = label_file
            print 'Label File: ', label_file
        else:
            print 'Nothing has been selected!'

    def _sessid_file_browse(self):
        sessid_file = self._open_file_dialog("SessID File")
        if sessid_file:
            self._sessid_file_dir.setText(sessid_file)
            self.sessid_file = sessid_file
            print 'Seg. File: ', sessid_file
        else:
            print 'Nothing has been selected!'

    def _calculate_MBN_checked(self):
        if self._calculate_population_based_mbn_check.isChecked():
            print 'Calculate population-based MBN has been checked. '
        else:
            print 'Calculate population-based MBN cancled check status. '
