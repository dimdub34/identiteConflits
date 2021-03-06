# -*- coding: utf-8 -*-

import logging
import random

from twisted.internet import defer
from client.cltremote import IRemote
from client.cltgui.cltguidialogs import GuiRecapitulatif
import identiteConflitsParams as pms
from identiteConflitsGui import GuiDecision
import identiteConflitsTexts as texts_IC


logger = logging.getLogger("le2m")


class RemoteIC(IRemote):
    """
    Class remote, remote_ methods can be called by the server
    """
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)
        self._histo_vars = [
            "IC_period", "IC_decision",
            "IC_periodpayoff", "IC_cumulativepayoff"]
        self._histo.append(texts_IC.get_histo_head())

    def remote_configure(self, params):
        """
        Set the same parameters as in the server side
        :param params:
        :return:
        """
        logger.info(u"{} configure".format(self._le2mclt.uid))
        for k, v in params.viewitems():
            setattr(pms, k, v)

    def remote_newperiod(self, period):
        """
        Set the current period and delete the history
        :param period: the current period
        :return:
        """
        logger.info(u"{} Period {}".format(self._le2mclt.uid, period))
        self.currentperiod = period
        if self.currentperiod == 1:
            del self.histo[1:]

    def remote_set_identities(self, identity_1, identity_2, identity_combined):
        self._identity_1 = identity_1
        self._identity_2 = identity_2
        self._identity_combined = identity_combined

    def remote_display_decision(self, q_type, q_num):
        """
        Display the decision screen
        :return: deferred
        """
        logger.info(u"{} Decision".format(self._le2mclt.uid))

        # get the matrix
        if q_type == pms.MIXED and q_num > 6:
            mat = pms.MATRIX.get(q_num - 6)
            matrice = [(j, i) for i, j in mat]
        else:
            matrice = pms.MATRIX.get(q_num)

        if self._le2mclt.simulation:
            decision = matrice.index(random.choice(matrice))
            logger.info(u"{} Send back {}".format(self._le2mclt.uid, decision))
            return decision

        else:
            txt_expl, labels = texts_IC.get_txt_expl_decision(
                self._identity_1, self._identity_combined, q_type)
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered, self._le2mclt.automatique,
                self._le2mclt.screen, txt_expl, labels, matrice)
            ecran_decision.show()
            return defered
