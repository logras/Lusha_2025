#!/user/bin/env python3
# @IDE         PyCharm
# @Project     selenium
# @Filename    test_cases.py
# @Directory   structured_pom/utils
# @Author      belr
# @Date        13/10/2022
"""
We should add test cases here because we can miss some cases while writing automation code or
some manuel testers (test analystes) can handle this more efficiently.
We can obtain test cases from test management :
http://www.inflectra.com/SpiraTest/Integrations/Unit-Test-Frameworks.aspx
We can also record the result of test cases to test management tool.
"""
# -----------------------------------------------------------------------------
# Copyright (c) 2015, the IPython Development Team and José Fonseca.
#
# Distributed under the terms of the Creative Commons License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#
#
# REFERENCES:
# http://ipython.org/ipython-doc/rel-0.13.2/development/coding_guide.html
# https://www.python.org/dev/peps/pep-0008/
# -----------------------------------------------------------------------------
'''
OPTIONS ------------------------------------------------------------------
A description of each option that can be passed to this script
ARGUMENTS -------------------------------------------------------------
A description of each argument that can or must be passed to this script
'''
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

# stdlib imports -------------------------------------------------------

# Third-party imports -----------------------------------------------
import pytest

# Our own imports ---------------------------------------------------

# -----------------------------------------------------------------------------
# GLOBALS
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# LOCAL UTILITIES
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# CLASSES
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------
def formal_test_cases(number):
    return testCases[number]


# for maintainability, we can seperate web test cases by page name but I just listed every case in same array
testCases = [
    # [
    #     severity,
    #     description
    # ]
    [
        'Blocker',
        'when user goes to main page, page should be loaded'
    ],
    [
        'Blocker',
        'In "Main" page, when user click "Les notes de frais" button, he should see the "Notes de frais" page'
    ],
    [
        'Blocker',
        'In "Les notes de frais" page, when user click "Nouvelle note" button, he should see "Nouvelle note" Page'
    ],
    [
        'Blocker',
        'In "Nouvelle note" page, user can fill in the form & click "Soumettre" button for validation'
    ],
    [
        'Blocker',
        'In "Login" Page, when user log in with a VALID user, he should see "Main" Page'
    ],
    [
        'Blocker',
        'In "Login" Page, when user log in with an INVALID user, he should see Error Message'
    ],
]
