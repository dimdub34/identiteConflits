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

        for i in range(28):
            txt = str(valeurs[i/2][0] if i % 2 else valeurs[i/2][1])
            button = QtGui.QPushButton(txt)
            button.setFixedSize(20, 15)
            button.setFlat(True)
            button.setObjectName("button_{}".format(i))
            setattr(self, "button_{}".format(i), button)
            layout.addWidget(button, i % 2, (i / 2) + 1)

        self.adjustSize()


class Saisies(QtGui.QWidget):
    def __init__(self, the_labels, automatique):
        QtGui.QWidget.__init__(self)

        self._automatique = automatique

        layout = QtGui.QGridLayout(self)

        label_haut = QtGui.QLabel(the_labels[0])
        layout.addWidget(label_haut, 0, 0)
        label_bas = QtGui.QLabel(the_labels[1])
        layout.addWidget(label_bas, 1, 0)

        self._dec_haut = WSpinbox(u"", 0, 50, self._automatique)
        layout.addWidget(self._dec_haut, 0, 1)
        self._dec_bas = WSpinbox(u"", 0, 50, self._automatique)
        layout.addWidget(self._dec_bas, 1, 1)

        self.adjustSize()

    def get_values(self):
        return (self._dec_haut.get_value(), self._dec_bas.get_value())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    labels = (u"Une personne rouge", u"Une personne non-rouge")
    valeurs = [(random.randint(1, 30), random.randint(1, 30)) for _ in range(14)]
    # mat = Matrice(labels, valeurs)
    # mat.show()
    sais = Saisies(labels, False)
    sais.show()
    sys.exit(app.exec_())