# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools
from util.utili18n import le2mtrans
import identiteConflitsParams as pms


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen)
        actions = OrderedDict()
        actions[le2mtrans(u"Configure")] = self._configure
        actions[le2mtrans(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), le2mtrans(u"Parameters"))
        actions[le2mtrans(u"Start") + u" identité simple"] = \
            lambda _: self._demarrer(pms.get_treatment("simple"))
        actions[le2mtrans(u"Start") + u" identité double"] = \
            lambda _: self._demarrer(pms.get_treatment("double"))
        actions[le2mtrans(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs_onserver("identiteConflits")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Identité et conflits", actions)

    def _configure(self):
        self._le2mserv.gestionnaire_graphique.display_information(
            le2mtrans(u"There is no parameter to configure"))
        return

    @defer.inlineCallbacks
    def _demarrer(self, treatment):
        """
        Start the part
        :return:
        """
        pms.TREATMENT = treatment

        # check conditions =====================================================
        # nb of players and group size
        if self._le2mserv.gestionnaire_joueurs.nombre_joueurs % 4 != 0:
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Nombre de joueurs non multiple de 4")
            return
        else:
            pms.TAILLE_GROUPES = \
                self._le2mserv.gestionnaire_joueurs.nombre_joueurs / 4

        # confirmation
        if not self._le2mserv.gestionnaire_graphique.question(
                        le2mtrans(u"Start") +
                        u" identiteConflits (treatment identité {})?".format(
                            pms.get_treatment(pms.TREATMENT))):
            return

        # init part ============================================================
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "identiteConflits", "PartieIC",
            "RemoteIC", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'identiteConflits')

        # set parameters on remotes
        yield (self._le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Configure"), self._tous, "configure"))
        
        # form groups
        try:
            self._le2mserv.gestionnaire_groupes.former_groupes(
                self._le2mserv.gestionnaire_joueurs.get_players(),
                pms.TAILLE_GROUPES, forcer_nouveaux=False)
        except ValueError as e:
            self._le2mserv.gestionnaire_graphique.display_error(
                e.message)
            return
    
        # Start part ===========================================================
        for period in range(1 if pms.NOMBRE_PERIODES else 0,
                        pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # init period
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, le2mtrans(u"Period") + u" {}".format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, le2mtrans(u"Period") + u" {}".format(period)],
                fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))
            
            # decision
            yield(self._le2mserv.gestionnaire_experience.run_step(
                le2mtrans(u"Decision"), self._tous, "display_decision"))
            
            # period payoffs
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "identiteConflits")
        
            # summary
            yield(self._le2mserv.gestionnaire_experience.run_step(
                le2mtrans(u"Summary"), self._tous, "display_summary"))
        
        # End of part ==========================================================
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "identiteConflits"))
