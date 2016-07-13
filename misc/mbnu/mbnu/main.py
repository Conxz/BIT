# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from MBNUDialog import MBNUDialog


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MBNUDialog()
    form.show()
    app.exec_()