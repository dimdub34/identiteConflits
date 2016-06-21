# -*- coding: utf-8 -*-
"""
This module contains the GUI
"""

import logging
from PyQt4 import QtGui, QtCore
from util.utili18n import le2mtrans
import identiteConflitsParams as pms
from identiteConflitsTexts import trans_IC
from client.cltgui.cltguiwidgets import WExplication
from identiteConflitsWidget import Matrice, Saisies


logger = logging.getLogger("le2m")


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, txt_expl, labels, valeurs):
        super(GuiDecision, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique
        self._valeurs = valeurs

        layout = QtGui.QVBoxLayout(self)

        wexplanation = WExplication(
            text=txt_expl,
            size=(450, 80), parent=self)
        layout.addWidget(wexplanation)

        wmatrice = Matrice(labels, valeurs)
        layout.addWidget(wmatrice)

        self._wdecision = Saisies(labels, self._automatique)
        layout.addWidget(self._wdecision)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(trans_IC(u"Title"))
        self.adjustSize()
        self.setFixedSize(self.size())

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)
                
    def reject(self):
        pass
    
    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        vals = self._wdecision.get_values()
        if vals not in self._valeurs:
            QtGui.QMessageBox.warning(
                self, u"Attention", u"Au moins une des valeurs saisies n'est "
                                    u"pas dans la matrice proposée")
            return
        decision = self._valeurs.index(vals)
        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your choice?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        logger.info(u"Send back {} ({})".format(decision, vals))
        self.accept()
        self._defered.callback(decision)
