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
import random


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
            size=(450, 120), parent=self, html=True)
        layout.addWidget(wexplanation)

        random_repart = None
        if self._automatique:
            random_vals = random.choice(valeurs)
            random_repart = valeurs.index(random_vals)

        self._wmatrice = Matrice(labels, valeurs, self._automatique,
                                 random_repart=random_repart)
        layout.addWidget(self._wmatrice)

        # decision (inside an horizontal layout)
        lay_wdec = QtGui.QHBoxLayout()
        lay_wdec.addSpacerItem(
            QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Expanding))
        self._wdecision = Saisies(labels, valeurs, self._automatique,
                                  random_repart=random_repart)
        lay_wdec.addWidget(self._wdecision)
        lay_wdec.addSpacerItem(
            QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Expanding))
        layout.addLayout(lay_wdec)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(trans_IC(u"Décision"))
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

        selec = self._wmatrice.get_selected()
        if selec < 0:
            QtGui.QMessageBox.warning(
                self, u"Attention", u"Veuillez sélectionner une répartition")
            return

        vals = self._wdecision.get_values()
        if vals not in self._valeurs:
            QtGui.QMessageBox.warning(
                self, u"Attention", u"Au moins une des valeurs saisies n'est "
                                    u"pas dans la matrice proposée")
            return

        decision = self._valeurs.index(vals)
        if selec != decision:
            QtGui.QMessageBox.warning(
                self, u"Attention", u"La répartition sélectionnée ne correspond "
                                    u"pas aux valeurs saisies")
            return

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
