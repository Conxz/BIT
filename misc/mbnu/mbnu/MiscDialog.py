# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MiscDialog(QDialog):
    def __init__(self, parent=None):
        super(MiscDialog, self).__init__(parent)
        self.setWindowTitle("This dialog is just for fun or anything else? :)")

        self._init_gui()
        self._create_actions()

    def _init_gui(self):
        pass



    def _create_actions(self):
        pass



