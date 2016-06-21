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
    elif identity == pms.ID1E:
        return u"non-jaune"
    elif identity == pms.ID2:
        return u"carré"
    elif identity == pms.ID2E:
        return u"non-carré"
    elif identity == pms.ID1__ID2:
        return u"jaune et carré"
    elif identity == pms.ID1__ID2E:
        return u"jaune et non-carré"
    elif identity == pms.ID1E__ID2:
        return u"non-jaune et carré"
    else:
        return u"non-jaune et non-carré"


def get_histo_head():
    return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
             le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]


def get_txt_expl_decision(id_or_combined, q_type):
    """
    :param id_or_combined:
    :param q_type:
    :return:
    """

    txt = u"Vous êtes dans le groupe {}.\n".format(
        get_txt_identity(id_or_combined))

    txt += u"Vous devez choisir une répartition entre "

    if q_type == pms.SAME:
        txt += u"deux personnes du groupe {}.".format(
            get_txt_expl_decision(id_or_combined))
        labels = (u"Une personne " + get_txt_identity(id_or_combined),
                  u"Une personne " + get_txt_identity(id_or_combined))

    elif q_type == pms.MIXED:
        txt += u"une personne du groupe {} et une personne qui n'est pas dans " \
               u"ce groupe.".format(get_txt_identity(id_or_combined))
        labels = (u"Une personne " + get_txt_identity(id_or_combined),
                  u"Une personne qui n'est pas " + get_txt_identity(
                      id_or_combined))

    else:
        txt += u"deux personnes qui ne sont pas dans le groupe {}.".format(
            get_txt_identity(id_or_combined))
        labels = (u"Une personne qui n'est pas " + get_txt_identity(
                      id_or_combined), u"Une personne qui n'est pas " +
                  get_txt_identity(id_or_combined))

    return txt, labels


# def get_text_summary(period_content):
#     txt = trans_IC(u"Summary text")
#     return txt


