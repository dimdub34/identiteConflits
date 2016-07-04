#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore


class MyWidget(QtGui.QWidget):

    clicked = QtCore.pyqtSignal()

    def __init__(self, number, matrice):
        QtGui.QWidget.__init__(self)

        self._number = number

        lay = QtGui.QVBoxLayout(self)
        lab_top = QtGui.QLabel(str(matrice[0]))
        lab_top.setAlignment(QtCore.Qt.AlignRight)
        lay.addWidget(lab_top)
        lab_bot = QtGui.QLabel(str(matrice[1]))
        lab_bot.setAlignment(QtCore.Qt.AlignRight)
        lay.addWidget(lab_bot)

        self.setFixedSize(30, 60)
        self.setStyleSheet("font-weight: bold;")
        self.set_selected(False)

    @property
    def number(self):
        return self._number

    def mouseReleaseEvent(self, event):
        self.clicked.emit()
        event.accept()

    def set_selected(self, true_or_false):
        if true_or_false:
            self.setStyleSheet("color:blue;")
        else:
            self.setStyleSheet("color: black;")


class Matrice(QtGui.QWidget):
    def __init__(self, labels, valeurs, automatique, random_repart=None):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QHBoxLayout(self)

        widget_lab = QtGui.QWidget()
        widget_lab_lay = QtGui.QVBoxLayout(widget_lab)
        lab_top = QtGui.QLabel(labels[0])
        lab_top.setAlignment(QtCore.Qt.AlignRight)
        widget_lab_lay.addWidget(lab_top)
        lab_bot = QtGui.QLabel(labels[1])
        lab_bot.setAlignment(QtCore.Qt.AlignRight)
        widget_lab_lay.addWidget(lab_bot)
        widget_lab.setFixedSize(200, 50)
        layout.addWidget(widget_lab)

        self._selected = -1
        self._list_widget_mat = []

        for i, val in enumerate(valeurs):
            widget_mat = MyWidget(i, val)
            widget_mat.clicked.connect(self._set_selected)
            self._list_widget_mat.append(widget_mat)
            layout.addWidget(widget_mat)

        self.adjustSize()

        if automatique:
            self._list_widget_mat[random_repart].set_selected(True)
            self._selected = random_repart

    def _set_selected(self):
        for wid in self._list_widget_mat:
            if self.sender() == wid:
                wid.set_selected(True)
                self._selected = wid.number
            else:
                wid.set_selected(False)

    def get_selected(self):
        return self._selected


class Saisies(QtGui.QWidget):
    def __init__(self, labels, valeurs, automatique, random_repart=None):
        QtGui.QWidget.__init__(self)

        layout = QtGui.QGridLayout(self)

        label_haut = QtGui.QLabel(labels[0])
        layout.addWidget(label_haut, 0, 0)
        self._dec_haut = QtGui.QSpinBox()
        self._dec_haut.setMinimum(0)
        self._dec_haut.setMaximum(100)
        self._dec_haut.setSingleStep(1)
        self._dec_haut.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        lay_dec_top = QtGui.QHBoxLayout()
        lay_dec_top.addWidget(self._dec_haut)
        lay_dec_top.addSpacerItem(
            QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Expanding))
        layout.addLayout(lay_dec_top, 0, 1)
        
        label_bas = QtGui.QLabel(labels[1])
        layout.addWidget(label_bas, 1, 0)
        self._dec_bas = QtGui.QSpinBox()
        self._dec_bas.setMinimum(0)
        self._dec_bas.setMaximum(100)
        self._dec_bas.setSingleStep(1)
        self._dec_bas.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        lay_dec_bot = QtGui.QHBoxLayout()
        lay_dec_bot.addWidget(self._dec_bas)
        lay_dec_bot.addSpacerItem(
            QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Expanding))
        layout.addLayout(lay_dec_bot, 1, 1)

        self.adjustSize()

        if automatique:
            sel = valeurs[random_repart]
            self._dec_haut.setValue(sel[0])
            self._dec_bas.setValue(sel[1])

    def get_values(self):
        return self._dec_haut.value(), self._dec_bas.value()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    labels = (u"Une personne identifiée comme vous",
              u"Une personne pas identifiée comme vous")
    valeurs = zip(range(1, 15), range(14, 0, -1))
    mat = Matrice(labels, valeurs, False)
    mat.show()
    sais = Saisies(labels, valeurs, False)
    sais.show()
    sys.exit(app.exec_())