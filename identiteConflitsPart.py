# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
from server.servbase import Base
from server.servparties import Partie
from util.utiltools import get_module_attributes
import identiteConflitsParams as pms
from random import randint


logger = logging.getLogger("le2m")


class PartieIC(Partie):
    __tablename__ = "partie_identiteConflits"
    __mapper_args__ = {'polymorphic_identity': 'identiteConflits'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsIC')

    def __init__(self, le2mserv, joueur):
        super(PartieIC, self).__init__(
            nom="identiteConflits", nom_court="IC",
            joueur=joueur, le2mserv=le2mserv)

        self._current_sequence = 0
        self._id1 = 0
        self._id2 = 0
        self._id_combined = 0
        self._data = {}

        self.IC_gain_ecus = 0
        self.IC_gain_euros = 0

    @property
    def data(self):
        return self._data

    @defer.inlineCallbacks
    def configure(self, current_sequence):
        logger.debug(u"{} Configure".format(self.joueur))
        self._current_sequence = current_sequence
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))
        self.joueur.info(u"Ok")

    @defer.inlineCallbacks
    def set_identities(self, id1, id2):
        """
        Set both identities and determines the combined one
        :param id1:
        :param id2:
        :return:
        """
        self._id1 = id1
        self._id2 = id2
        if self._id1 == pms.ID1:
            if self._id2 == pms.ID2:
                self._id_combined = pms.ID1__ID2
            else:
                self._id_combined = pms.ID1__ID2E
        else:
            if self._id2 == pms.ID2:
                self._id_combined = pms.ID1E__ID2
            else:
                self._id_combined = pms.ID1E__ID2E
        yield (self.remote.callRemote(
            "set_identities", self._id1, self._id2, self._id_combined))

    @defer.inlineCallbacks
    def newperiod(self, period):
        """
        Create a new period and inform the remote
        If this is the first period then clear the historic
        :param period:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        self.currentperiod = RepetitionsIC(period)
        self.currentperiod.IC_sequence = self._current_sequence
        self.currentperiod.IC_treatment = pms.TREATMENT
        self.currentperiod.IC_identity_1 = self._id1
        self.currentperiod.IC_identity_2 = self._id2
        self.currentperiod.IC_identity_combined = self._id_combined
        self.le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for period {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_decision(self):
        """
        Display the decision screen on the remote
        Get back the decision
        :return:
        """
        logger.debug(u"{} Decision".format(self.joueur))
        # set the order
        self.currentperiod.IC_order = randint(1, 3)
        order = getattr(pms, "ORDER_{}".format(self.currentperiod.IC_order))[:]

        debut = datetime.now()
        for q in order:
            q_type, q_num = q.split("_")
            q_type = pms.SAME if q_type == "s" else pms.MIXED if q_type == "m" \
                else pms.DIFFERENT
            q_dec = "same" if q_type == pms.SAME else "mixed" if \
                q_type == pms.MIXED else "different"
            logger.debug(u"{} - {} -> ({}, {})".format(
                self.joueur, q, q_dec, q_num))
            dec = yield(self.remote.callRemote(
                "display_decision", q_type, int(q_num)))
            setattr(self.currentperiod,
                    "IC_decision_{}_{}".format(q_dec, q_num), dec)
            self.joueur.info(u"{}_{} - {}".format(q_dec, q_num, dec))
        self.currentperiod.ID_decision_time = (datetime.now() - debut).seconds
        self.joueur.remove_waitmode()

    def set_payoff(self, decideur, q_seq, q_type, q_mat, q_values, decideur_dec,
                   gain):
        logger.debug(u"{}: {}, {}, {}, {}, {}, {}, {}".format(
            self.joueur, decideur, q_seq, q_type, q_mat, q_values, decideur_dec,
            gain))
        self.IC_gain_ecus = gain
        self.joueur.info(
            u"décideur {} - seq {} - type {} - mat {} - choix {} - gain {}".format(
                decideur, q_seq, q_type, q_mat, decideur_dec, gain))

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.IC_periodpayoff = 0

        # cumulative payoff since the first period
        if self.currentperiod.IC_period < 2:
            self.currentperiod.IC_cumulativepayoff = \
                self.currentperiod.IC_periodpayoff
        else:
            previousperiod = self.periods[self.currentperiod.IC_period - 1]
            self.currentperiod.IC_cumulativepayoff = \
                previousperiod.IC_cumulativepayoff + \
                self.currentperiod.IC_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.periods[self.currentperiod.IC_period] = self.currentperiod
        self._data[self._current_sequence] = self.periods

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur,
            self.currentperiod.IC_periodpayoff))

    # @defer.inlineCallbacks
    def display_summary(self):
        """
        Send a dictionary with the period content values to the remote.
        The remote creates the text and the history
        :param args:
        :return:
        """
        logger.debug(u"{} Summary".format(self.joueur))
        # yield(self.remote.callRemote(
        #     "display_summary", self.currentperiod.todict()))
        dec_same = [getattr(self.currentperiod, "IC_decision_same_{}".format(i))
                    for i in range(1, 7)]
        self.joueur.info(u"Same {}".format(dec_same))
        dec_mixed = [getattr(self.currentperiod, "IC_decision_mixed_{}".format(i))
                    for i in range(1, 13)]
        self.joueur.info(u"Mixed {}".format(dec_mixed))
        dec_different = [getattr(self.currentperiod, "IC_decision_different_{}".format(i))
                    for i in range(1, 7)]
        self.joueur.info(u"Different {}".format(dec_different))
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def compute_partpayoff(self):
        """
        Compute the payoff for the part and set it on the remote.
        The remote stores it and creates the corresponding text for display
        (if asked)
        :return:
        """
        logger.debug(u"{} Part Payoff".format(self.joueur))

        # self.IC_gain_ecus = self.currentperiod.IC_cumulativepayoff
        self.IC_gain_euros = float(self.IC_gain_ecus) * float(pms.TAUX_CONVERSION)
        yield (self.remote.callRemote(
            "set_payoffs", self.IC_gain_euros, self.IC_gain_ecus))

        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.IC_gain_ecus, self.IC_gain_euros))


class RepetitionsIC(Base):
    __tablename__ = 'partie_identiteConflits_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_identiteConflits.partie_id"))

    IC_sequence = Column(Integer)
    IC_order = Column(Integer)
    IC_period = Column(Integer)
    IC_treatment = Column(Integer)
    IC_identity_1 = Column(Integer)
    IC_identity_2 = Column(Integer)
    IC_identity_combined = Column(Integer)
    IC_decision_same_1 = Column(Integer)
    IC_decision_same_2 = Column(Integer)
    IC_decision_same_3 = Column(Integer)
    IC_decision_same_4 = Column(Integer)
    IC_decision_same_5 = Column(Integer)
    IC_decision_same_6 = Column(Integer)
    IC_decision_mixed_1 = Column(Integer)
    IC_decision_mixed_2 = Column(Integer)
    IC_decision_mixed_3 = Column(Integer)
    IC_decision_mixed_4 = Column(Integer)
    IC_decision_mixed_5 = Column(Integer)
    IC_decision_mixed_6 = Column(Integer)
    IC_decision_mixed_7 = Column(Integer)
    IC_decision_mixed_8 = Column(Integer)
    IC_decision_mixed_9 = Column(Integer)
    IC_decision_mixed_10 = Column(Integer)
    IC_decision_mixed_11 = Column(Integer)
    IC_decision_mixed_12 = Column(Integer)
    IC_decision_different_1 = Column(Integer)
    IC_decision_different_2 = Column(Integer)
    IC_decision_different_3 = Column(Integer)
    IC_decision_different_4 = Column(Integer)
    IC_decision_different_5 = Column(Integer)
    IC_decision_different_6 = Column(Integer)
    ID_decision_time = Column(Integer)
    IC_periodpayoff = Column(Float)
    IC_cumulativepayoff = Column(Float)

    def __init__(self, period):
        self.IC_period = period
        self.IC_decisiontime = 0
        self.IC_periodpayoff = 0
        self.IC_cumulativepayoff = 0

    def todict(self, joueur=None):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if joueur:
            temp["joueur"] = joueur
        return temp

