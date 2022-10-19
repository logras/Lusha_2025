#!/user/bin/env python3
# @IDE         PyCharm
# @Project     selenium
# @Filename    users.py
# @Directory   structured_pom/utils
# @Author      belr
# @Date        13/10/2022
"""Users for testing."""
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
import decouple

# Third-party imports -----------------------------------------------
# from operator import itemgetter

# Our own imports ---------------------------------------------------

# -----------------------------------------------------------------------------
# GLOBALS
# -----------------------------------------------------------------------------
# VALID_USER_LOGIN = decouple.config('KIWIHR_LOGIN', default='sovucas.fepaqe@jollyfree.com')
VALID_USER_LOGIN = decouple.config('KIWIHR_LOGIN', default='<your_default_kiwihr_username_here>')
# VALID_USER_PASSWORD = decouple.config('KIWIHR_PASSWORD', default='M2I_n1@2022')
VALID_USER_PASSWORD = decouple.config(
    'KIWIHR_PASSWORD',
    default='<your_default_kiwihr_password_here>'
    )

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
def get_user(name):
    try:
        return next(user for user in users if user["name"] == name)
    except Exception as e:
        logger.append(str(e))
        print("\n     User %s is not defined, enter a valid user.\n" % name)


logger = []

# we can store test data in this module like users
users = [
    {"name": "invalid_user", "email": "invalidUser@test.com", "password": "qwert1235"},
    {"name": "valid_user", "email": VALID_USER_LOGIN, "password": VALID_USER_PASSWORD},
    # {"name": "Staff2", "email": "staff@test.com", "password": "qwert1235"},
    # {"name": "Admin0", "email": "admin@test.com", "password": "qwert1234"},
    # {"name": "Admin1", "email": "admin@test.com", "password": "qwert1234"},
    # {"name": "Admin2", "email": "admin@test.com", "password": "qwert1234"},
]
