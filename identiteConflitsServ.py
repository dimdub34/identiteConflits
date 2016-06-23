# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools
from util.utili18n import le2mtrans
import identiteConflitsParams as pms
import random


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv
        self._current_sequence = 0

        # creation of the menu (will be placed in the "part" menu on the
        # server screen)
        actions = OrderedDict()
        actions[le2mtrans(u"Configure")] = self._configure
        actions[le2mtrans(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), le2mtrans(u"Parameters"))
        actions[le2mtrans(u"Start") + u" mono-identité"] = \
            lambda _: self._demarrer(pms.MONO)
        actions[le2mtrans(u"Start") + u" double-identité"] = \
            lambda _: self._demarrer(pms.DOUBLE)
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
        :param treatment the treatment to start
        :return:
        """

        pms.TREATMENT = treatment

        # ======================================================================
        #
        # check conditions
        #
        # ======================================================================

        # nb of players and group size
        if self._le2mserv.gestionnaire_joueurs.nombre_joueurs % 4 != 0:
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Nombre de joueurs non multiple de 4")
            return

        # confirmation
        if not self._le2mserv.gestionnaire_graphique.question(
                        le2mtrans(u"Start") +
                        u" identiteConflits (treatment identité {})?".format(
                            pms.get_treatment(pms.TREATMENT))):
            return

        # ======================================================================
        #
        # init part
        #
        # ======================================================================

        self._current_sequence += 1

        yield (self._le2mserv.gestionnaire_experience.init_part(
            "identiteConflits", "PartieIC",
            "RemoteIC", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'identiteConflits')

        # infos on server list
        self._le2mserv.gestionnaire_graphique.infoserv(
            [u"Sequence {}".format(self._current_sequence),
             u"Treatment {}".format(pms.get_treatment(pms.TREATMENT))])

        # set parameters on remotes
        yield (self._le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Configure"), self._tous, "configure",
            self._current_sequence))

        # ======================================================================
        #
        # set identities - only if first sequence
        # we set both identities directly
        #
        # ======================================================================

        players = [p.get_part("identiteConflits") for p in
                   self._le2mserv.gestionnaire_joueurs.get_players()]

        if self._current_sequence == 1:
            # id1
            self._tous__id1 = players[: len(players)/2]
            self._tous__id1e = players[len(players)/2:]
            # id2
            self._tous__id2 = self._tous__id1[: len(self._tous__id1)/2] + \
                        self._tous__id1e[: len(self._tous__id1e)/2]
            self._tous__id2e = self._tous__id1[len(self._tous__id1)/2:] + \
                        self._tous__id1e[len(self._tous__id1e)/2:]
            # combined
            self._tous__id1_id2 = [p for p in players if p in self._tous__id1
                                   and p in self._tous__id2]
            self._tous__id1_id2e = [p for p in players if p in self._tous__id1
                                   and p in self._tous__id2e]
            self._tous__id1e_id2 = [p for p in players if p in self._tous__id1e
                                   and p in self._tous__id2]
            self._tous__id1e_id2e = [p for p in players if p in self._tous__id1e
                                   and p in self._tous__id2e]

        # seq 1 or 2, we set the identities in the players' data
        for p in players:
            p.set_identities(
                pms.ID1 if p in self._tous__id1 else pms.ID1E,
                pms.ID2 if p in self._tous__id2 else pms.ID2E
            )

        # display on server
        def get_players(list_parts):
            return u"{}".format([part.joueur for part in list_parts])

        self._le2mserv.gestionnaire_graphique.infoserv(
            [u"ID1", get_players(self._tous__id1), None,
             u"ID1E", get_players(self._tous__id1e), None,
             u"ID2", get_players(self._tous__id2), None, u"ID2E",
             get_players(self._tous__id2e), None, u"Combined", u"ID1_ID2",
             get_players(self._tous__id1_id2), u"ID1_ID2E",
             get_players(self._tous__id1_id2e), u"ID1E_ID2",
             get_players(self._tous__id1e_id2), u"ID1E_ID2E",
             get_players(self._tous__id1e_id2e)])

        # ======================================================================
        #
        # Start part
        #
        # ======================================================================
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

            # summary (only on the server side for this experiment)
            self._le2mserv.gestionnaire_experience.run_step(
                le2mtrans(u"Summary"), self._tous, "display_summary")

        # ======================================================================
        #
        # End of part
        #
        # ======================================================================

        self._le2mserv.gestionnaire_graphique.infoclt(
            u"Calcul des payoffs".upper())

        without_payoff = [j.get_part("identiteConflits") for j in
                          self._le2mserv.gestionnaire_joueurs.get_players()]
        pool_for_decisions = without_payoff[:]

        while without_payoff:

            q_seq = random.randint(1, self._current_sequence)
            q_type = random.choice([pms.SAME, pms.MIXED, pms.DIFFERENT])
            q_mat = random.randint(1, len(pms.MATRIX) * 2 if
                q_type == pms.MIXED else len(pms.MATRIX))
            logger.info(u"Payoff: {}, {}".format(q_type, q_mat))

            if q_mat > 6:
                q_values = pms.MATRIX.get(q_mat-6)[::-1]
            else:
                q_values = pms.MATRIX.get(q_mat)

            # we take one player at random (without removing it)
            player = random.choice(pool_for_decisions)
            player_data = player.data[q_seq][0]


            # MONO
            if pms.TREATMENT == pms.MONO:

                player_id = player_data.IC_identity_1
                pool_same = [p for p in without_payoff if
                               p.data[q_seq][0].IC_identity_1 == player_id]
                pool_diff = [p for p in without_payoff if
                               p.data[q_seq][0].IC_identity_1 != player_id]

            # DOUBLE
            else:
                player_id = player_data.IC_identity_combined
                pool_same = [p for p in without_payoff if
                             p.data[q_seq][0].IC_identity_combined == player_id]
                pool_diff = [p for p in without_payoff if
                             p.data[q_seq][0].IC_identity_combined != player_id]

            if q_type == pms.SAME:
                player_dec = getattr(player_data,
                                     "IC_decision_same_{}".format(q_mat))
                q_val = q_values[player_dec]
                try:
                    first = pool_same.pop()
                    first.set_payoff(player.joueur, q_seq, q_type, q_mat,
                                     q_values, player_dec, q_val[0])
                    without_payoff.remove(first)
                except IndexError:  # no more
                    pass
                try:
                    second = pool_same.pop()
                    second.set_payoff(player.joueur, q_seq, q_type, q_mat,
                                      q_values, player_dec, q_val[1])
                    without_payoff.remove(second)
                except IndexError:  # no more
                    pass

            elif q_type == pms.MIXED:
                player_dec = getattr(player_data,
                                     "IC_decision_mixed_{}".format(q_mat))
                q_val = q_values[player_dec]
                try:
                    first = pool_same.pop()
                    first.set_payoff(player.joueur, q_seq, q_type, q_mat,
                                     q_values, player_dec, q_val[0])
                    without_payoff.remove(first)
                except IndexError:  # no more
                    pass
                try:
                    second = pool_diff.pop()
                    second.set_payoff(player.joueur, q_seq, q_type, q_mat,
                                      q_values, player_dec, q_val[1])
                    without_payoff.remove(second)
                except IndexError:  # no more
                    pass

            else:  # DIFFERENT
                player_dec = getattr(player_data,
                                     "IC_decision_different_{}".format(q_mat))
                q_val = q_values[player_dec]
                try:
                    first = pool_diff.pop()
                    first.set_payoff(player.joueur, q_seq, q_type, q_mat,
                                     q_values, player_dec, q_val[0])
                    without_payoff.remove(first)
                except IndexError:  # no more
                    pass
                try:
                    second = pool_diff.pop()
                    second.set_payoff(player.joueur, q_seq, q_type, q_mat,
                                      q_values, player_dec, q_val[1])
                    without_payoff.remove(second)
                except IndexError:  # no more
                    pass

        # finalize
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "identiteConflits"))
