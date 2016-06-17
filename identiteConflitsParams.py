# -*- coding: utf-8 -*-
"""=============================================================================
This modules contains the variables and the parameters.
Do not change the variables.
Parameters that can be changed without any risk of damages should be changed
by clicking on the configure sub-menu at the server screen.
If you need to change some parameters below please be sure of what you do,
which means that you should ask to the developer ;-)
============================================================================="""

# variables --------------------------------------------------------------------
TREATMENTS = {0: "simple", 1: "double"}


def get_treatment(code_or_name):
    if type(code_or_name) is int:
        return TREATMENTS.get(code_or_name, None)
    elif type(code_or_name) is str:
        for k, v in TREATMENTS.viewitems():
            if v.lower() == code_or_name.lower():
                return k
    return None


NO_RED = 0
RED = 1
NO_SQUARE = 0
SQUARE = 1
NO_RED__NO_SQUARE = 0
NO_RED__SQUARE = 1
RED__NO_SQUARE = 2
RED__SQUARE = 3
SAME = 0
MIXED = 1
DIFFERENT = 2

# parameters -------------------------------------------------------------------
TREATMENT = get_treatment("simple")  # changed by the program, don't touch
TAUX_CONVERSION = 1
NOMBRE_PERIODES = 0
TAILLE_GROUPES = 5
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"



