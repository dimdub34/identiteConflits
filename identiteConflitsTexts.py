# -*- coding: utf-8 -*-
"""
This module contains the texts of the part (server and remote)
"""

from util.utiltools import get_pluriel
import identiteConflitsParams as pms
from util.utili18n import le2mtrans
import os
import configuration.configparam as params
import gettext
import logging

logger = logging.getLogger("le2m")
localedir = os.path.join(params.getp("PARTSDIR"), "identiteConflits", "locale")
try:
    trans_IC = gettext.translation(
      "identiteConflits", localedir, languages=[params.getp("LANG")]).ugettext
except IOError:
    logger.critical(u"Translation file not found")
    trans_IC = lambda x: x  # if there is an error, no translation


def get_txt_identity(identity):
    if identity == pms.ID1:
        return u"jaune"
    else:
        return u"carré"


def get_histo_head():
    return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
             le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]


def get_txt_expl_decision(id1, idcomb, q_type):
    """
    :param id1: the first identity of the player
    :param idcomb: the combined identity (id1 and id1) of the player
    :param q_type: the type of the question
    :return:
    """
    id1_txt = get_txt_identity(pms.ID1)
    id2_txt = get_txt_identity(pms.ID2)

    txt = u"Vous êtes "

    # MONO
    if pms.TREATMENT == pms.MONO:
        if id1 == pms.ID1:
            txt += u"dans le groupe {}.".format(id1_txt)
        else:
            txt += u"exclu(e) du groupe {}.".format(id1_txt)

    # DOUBLE
    else:
        if idcomb == pms.ID1__ID2:
            txt += u"dans le groupe {} et dans le groupe {}.".format(
                id1_txt, id2_txt)
        elif idcomb == pms.ID1__ID2E:
            txt += u"dans le groupe {} mais exclu(e) du groupe {}.".format(
                id1_txt, id2_txt)
        elif idcomb == pms.ID1E__ID2:
            txt += u"exclu(e) du groupe {} mais dans le groupe {}.".format(
                id1_txt, id2_txt)
        else:
            txt += u"exclu(e) du groupe {} et exclu(e) du groupe {}.".format(
                id1_txt, id2_txt)


    txt += u" Vous devez choisir une répartition entre "

    # MONO =====================================================================
    if pms.TREATMENT == pms.MONO:

        if q_type == pms.SAME:

            if id1 == pms.ID1:
                txt += u"deux personnes du groupe {}.".format(
                    get_txt_identity(pms.ID1))
                labels = (u"Une personne du groupe " + id1_txt,
                          u"Une personne du groupe " + id1_txt)

            else:
                txt += u"deux personnes exclues du groupe {}.".format(
                    get_txt_identity(pms.ID1))
                labels = (u"Une personne exclue du groupe " + id1_txt,
                          u"Une personne exclue du groupe " + id1_txt)

        elif q_type == pms.MIXED:

            if id1 == pms.ID1:
                txt += u"une personne du groupe {0} et une personne exclue " \
                       u"du groupe {0}".format(id1_txt)
                labels = (u"Une personne du groupe " + id1_txt,
                          u"Une personne exclue du groupe " + id1_txt)
            else:
                txt += u"une personne exclue du groupe {0} et une personne " \
                       u"du groupe {0}".format(id1_txt)
                labels = (u"Une personne exclue du groupe " + id1_txt,
                          u"Une personne du groupe " + id1_txt)

        else:

            if id1 == pms.ID1:
                txt += u"deux personnes exclues du groupe {}.".format(id1_txt)
                labels = (u"Une personne exclue du groupe " + id1_txt,
                          u"Une personne exclue du groupe " + id1_txt)
            else:
                txt += u"deux personnes du groupe {}.".format(id1_txt)
                labels = (u"Une personne du groupe " + id1_txt,
                          u"Une personne du groupe " + id1_txt)

    # DOUBLE ===================================================================
    else:

        if q_type == pms.SAME: # -----------------------------------------------

            if idcomb == pms.ID1__ID2:
                txt += u"deux personnes simultanément du groupe " \
                       u"{} et {}.".format(id1_txt, id2_txt)
                labels = (u"Une personne du groupe {} et {}".format(id1_txt,
                                                                    id2_txt),
                          u"Une personne du groupe {} et {}".format(id1_txt,
                                                                    id2_txt))

            elif idcomb == pms.ID1__ID2E:
                txt += u"une personne du groupe {} et exclue du " \
                       u"groupe {}".format(id1_txt, id2_txt)
                labels = (u"Une personne du groupe {} et exclue du "
                          u"groupe {}".format(id1_txt, id2_txt),
                          u"Une personne du groupe {} et exclue du "
                          u"groupe {}".format(id1_txt, id2_txt))

            elif idcomb == pms.ID1E__ID2:
                txt += u"une personne exclue du groupe {} et mais dans le " \
                       u"groupe {}".format(id1_txt, id2_txt)
                labels = (u"Une personne exclue du groupe {} mais dans le  "
                          u"groupe {}".format(id1_txt, id2_txt),
                          u"Une personne exclue du groupe {} mais dans le "
                          u"groupe {}".format(id1_txt, id2_txt))

            else:
                txt += u"deux personnes simultanément exclues du groupe {} " \
                       u"et {}.".format(id1_txt, id2_txt)
                labels = (u"Une personne exclue du groupe {} et du "
                          u"groupe {}".format( id1_txt, id2_txt),
                          u"Une personne exclue du groupe {} et du "
                          u"groupe {}".format(id1_txt, id2_txt))

        elif q_type == pms.MIXED:  # -------------------------------------------

            if idcomb == pms.ID1__ID2:
                txt += u"une personne simultanément du groupe {} et {} et " \
                       u"une personne exclue d'au moins un de ces " \
                       u"groupes".format(id1_txt, id2_txt)
                labels = (u"Une personne du groupe {} et {}".format(
                    id1_txt, id2_txt),
                    u"Une personne exclue d'au moins un de ces groupes")

            elif idcomb == pms.ID1__ID2E:
                txt += u"une personne du groupe {0} et exclue du groupe {1} et " \
                       u"une personne qui n'est pas simultanément du groupe " \
                       u"{0} et exclue du groupe {1}".format(
                    id1_txt, id2_txt)
                labels = (u"une personne du groupe {} et exclue du "
                          u"groupe {}".format(id1_txt, id2_txt),
                          u"une personne qui n'est pas simultanément du groupe"
                          u"{} et exclue du groupe {}".format(id1_txt, id2_txt))

            elif idcomb == pms.ID1E__ID2:
                txt += u"une personne exclue du groupe {0} mais du groupe {1} " \
                       u"et une personne qui n'est pas simultanément exclue " \
                       u"du groupe {0} et du groupe {1}".format(
                    id1_txt, id2_txt)
                labels = (u"une personne exclue du groupe {} et du "
                          u"groupe {}".format(id1_txt, id2_txt),
                          u"une personne qui n'est pas simultanément exclue "
                          u"du groupe {} et du groupe {}".format(id1_txt, id2_txt))

            else:
                txt += u"une personne simultanément exclue du groupe {} et " \
                       u"du groupe {} et une personne qui est dans au moins " \
                       u"un des deux groupes".format(id1_txt, id2_txt)
                labels = (u"une personne simultanément exclue du groupe {} et " \
                       u"du groupe {}".format(id1_txt, id2_txt),
                          u"une personne qui est dans au moins un des "
                          u"deux groupes")

        # DIFFERENT ------------------------------------------------------------
        else:

            if idcomb == pms.ID1__ID2:
                txt += u"deux personnes exclues simultanément du groupe {} et " \
                       u"du groupe {}.".format(id1_txt, id2_txt)
                labels = (u"Une personne exclue simultanément du groupe {}"
                          u" et du groupe {}".format(id1_txt, id2_txt),
                          u"Une personne exclue simultanément du groupe {}"
                          u" et du groupe {}".format(id1_txt, id2_txt))

            elif idcomb == pms.ID1__ID2E:
                txt += u"deux personnes qui ne sont pas simultanément du " \
                       u"groupe {} et exclues du groupe {}".format(
                    id1_txt, id2_txt)
                labels = (u"une personne qui n'est pas simultanément du " \
                          u"groupe {} et exclue du groupe {}".format(
                    id1_txt, id2_txt),
                          u"une personne qui n'est pas simultanément du " \
                          u"groupe {} et exclue du groupe {}".format(
                              id1_txt, id2_txt))

            elif idcomb == pms.ID1E__ID2:
                txt += u"deux personnes qui ne sont pas simultanément exclues du " \
                       u"groupe {} mais dans le groupe {}".format(
                    id1_txt, id2_txt)
                labels = (u"une personne qui n'est pas simultanément exclue du " \
                          u"groupe {} mais dans le groupe {}".format(
                    id1_txt, id2_txt),
                          u"une personne qui n'est pas simultanément exclue du " \
                          u"groupe {} mais dans le groupe {}".format(
                              id1_txt, id2_txt))

            else:
                txt += u"deux personnes simultanément du groupe {} et " \
                       u"du groupe {}.".format(id1_txt, id2_txt)
                labels = (u"Une personne simultanément du groupe {}"
                          u" et du groupe {}".format(id1_txt, id2_txt),
                          u"Une personne simultanément du groupe {}"
                          u" et du groupe {}".format(id1_txt, id2_txt))

    return txt, labels


