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


def get_histo_head():
    return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
             le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]


def get_txt_expl_decision():
    return trans_IC(u"")


def get_text_summary(period_content):
    txt = trans_IC(u"Summary text")
    return txt


