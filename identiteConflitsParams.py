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
MONO = 0
DOUBLE = 1
TREATMENTS = {MONO: "mono", DOUBLE: "double"}


def get_treatment(code_or_name):
    if type(code_or_name) is int:
        return TREATMENTS.get(code_or_name, None)
    elif type(code_or_name) is str:
        for k, v in TREATMENTS.viewitems():
            if v.lower() == code_or_name.lower():
                return k
    return None

# identitites: E for Excluded
ID1E = 0
ID1 = 1
ID2E = 2
ID2 = 3

# combined
ID1E__ID2E = 0
ID1E__ID2 = 1
ID1__ID2E = 2
ID1__ID2 = 3

# kinds of repartitions
SAME = 0
MIXED = 1
DIFFERENT = 2

# parameters -------------------------------------------------------------------
TREATMENT = MONO  # changed by the program, don't touch
TAUX_CONVERSION = 1
NOMBRE_PERIODES = 0
MONNAIE = u"ecu"

# ==============================================================================
#
# There are 6 matrix (cf. Tajfel & al. 1971). From the article we keep only
# the matrix with positive values (experiment 1 and experiment 2)
#
# ==============================================================================
MATRIX = {
    1: zip(range(1, 15), range(14, 0, -1)),
    2: zip(range(18, 4, -1), range(5, 19)),
    3: zip(range(19, 6, -1), range(1, 26, 2)),
    4: zip(range(23, 10, -1), range(5, 30, 2)),
    5: zip(range(7, 20), range(1, 26, 2)),
    6: zip(range(11, 24), range(5, 30, 2))
}


# ==============================================================================
#
# These orders were set randomly on June 20th
# we consider 6 questions for SAME, 12 for MIXED (because of reverse order of
# the lines in the matrix) and 6 for DIFFERENT
# values = ['s_1', 's_2', 's_3', 's_4', 's_5', 's_6', 'm_1', 'm_2', 'm_3',
# 'm_4', 'm_5', 'm_6', 'm_7', 'm_8', 'm_9', 'm_10', 'm_11', 'm_12', 'd_1',
# 'd_2', 'd_3', 'd_4', 'd_5', 'd_6']
#
# ==============================================================================
ORDER_1 = ['m_6', 's_3', 'd_1', 's_5', 'm_11', 's_2', 'd_4', 'm_1', 's_6',
           'm_2', 'm_8', 'm_3', 'm_4', 'm_9', 'm_10', 's_1', 'm_5', 'd_2',
           'd_6', 'd_5', 'm_7', 'd_3', 'm_12', 's_4']

ORDER_2 = ['m_10', 'd_3', 's_1', 's_2', 'm_4', 'm_3', 'd_4', 's_4', 'm_8',
           'd_1', 'd_5', 'm_1', 'm_9', 'm_5', 's_5', 'm_11', 'd_6', 'd_2',
           'm_7', 'm_12', 's_3', 's_6', 'm_2', 'm_6']

ORDER_3 = ['d_1', 's_1', 'm_3', 's_5', 'm_5', 'm_11', 's_3', 'm_7', 'm_6',
           'm_10', 'm_8', 'd_4', 's_2', 'd_5', 's_6', 'd_6', 's_4', 'm_1',
           'm_9', 'm_12', 'd_2', 'm_2', 'm_4', 'd_3']