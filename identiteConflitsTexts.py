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


COM = 0
DIFF = 1


def get_txt_identity(identity):
    if identity == pms.ID1:
        return u"jaune"
    else:
        return u"carré"


def get_txt_personne(com_or_diff):
    if com_or_diff == COM:
        return u"personne identifiée exactement comme vous"
    else:
        return u"personne pas identifiée comme vous"


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
            txt += u"membre du groupe {}.".format(id1_txt)
        else:
            txt += u"exclu(e) du groupe {}.".format(id1_txt)

    # DOUBLE
    else:
        if idcomb == pms.ID1__ID2:
            txt += u"membre du groupe {} et membre du groupe {}.".format(
                id1_txt, id2_txt)
        elif idcomb == pms.ID1__ID2E:
            txt += u"membre du groupe {} et exclu(e) du groupe {}.".format(
                id1_txt, id2_txt)
        elif idcomb == pms.ID1E__ID2:
            txt += u"exclu(e) du groupe {} et membre du groupe {}.".format(
                id1_txt, id2_txt)
        else:
            txt += u"exclu(e) du groupe {} et exclu(e) du groupe {}.".format(
                id1_txt, id2_txt)

    txt += u"<br />" * 2
    txt += u"Vous devez choisir une répartition entre <strong>"

    if q_type == pms.SAME:
        txt += u"deux personnes identifiées exactement comme vous."
        labels = (get_txt_personne(COM), get_txt_personne(COM))

    elif q_type == pms.MIXED:
        txt += u"une personne identifiée exactement comme vous et une " \
               u"personne pas identifiée comme vous."
        labels = (get_txt_personne(COM), get_txt_personne(DIFF))

    else:
        txt += u"deux personnes pas identifiées comme vous."
        labels = (get_txt_personne(DIFF), get_txt_personne(DIFF))

    txt += u"</strong>"

    txt += u"<br />" * 2

    txt += u"Veuillez cliquer sur la répartition que vous choisissez " \
           u"(elle deviendra bleue) et saisir les valeurs correspondantes " \
           u"dans les zones de saisies en dessous."

    return txt, labels


