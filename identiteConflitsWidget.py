#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
import random
from client.cltgui.cltguiwidgets import WSpinbox


class Matrice(QtGui.QWidget):
    def __init__(self, labels, valeurs):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QGridLayout(self)

        label_haut = QtGui.QLabel(labels[0])
        layout.addWidget(label_haut, 0, 0)
        label_bas = QtGui.QLabel(labels[1])
        layout.addWidget(label_bas, 1, 0)

        for i, val in enumerate(valeurs):
            for b in range(2):
                btn = QtGui.QPushButton(str(val[b]))
                btn.setFixedSize(20, 15)
                btn.setFlat(True)
                btn.setObjectName("button_{}_{}".format(i, b))
                setattr(self, "button_{}_{}".format(i, b), btn)
                layout.addWidget(btn, b, i+1)

        self.adjustSize()


class Saisies(QtGui.QWidget):
    def __init__(self, labels, valeurs, automatique):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QGridLayout(self)

        label_haut = QtGui.QLabel(labels[0])
        layout.addWidget(label_haut, 0, 0)
        self._dec_haut = QtGui.QSpinBox()
        self._dec_haut.setMinimum(0)
        self._dec_haut.setMinimum(100)
        self._dec_haut.setSingleStep(1)
        self._dec_haut.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

        layout.addWidget(self._dec_haut, 0, 1)
        label_bas = QtGui.QLabel(labels[1])
        layout.addWidget(label_bas, 1, 0)
        self._dec_bas = QtGui.QSpinBox()
        layout.addWidget(self._dec_bas, 1, 1)

        self.adjustSize()

        if automatique:
            sel = random.choice(valeurs)
            self._dec_haut.ui.spinBox.setValue(sel[0])
            self._dec_bas.ui.spinBox.setValue(sel[1])

    def get_values(self):
        return self._dec_haut.get_value(), self._dec_bas.get_value()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    labels = (u"Une personne rouge", u"Une personne non-rouge")
    valeurs = zip(range(1, 15), range(14, 0, -1))
    # mat = Matrice(labels, valeurs)
    # mat.show()
    sais = Saisies(labels, valeurs, False)
    sais.show()
    sys.exit(app.exec_())