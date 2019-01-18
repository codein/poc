import os

GITHUB_OAUTH_TOKEN = 'GITHUB_OAUTH_TOKEN'

GITHUB_REPOSITORIES = [
    {

        'org': 'codein',
        'repo': 'poc'
    },
]


##################
# LOCAL SETTINGS #
##################

# DO NOT PLACE ANYTHING BELOW THIS!!!!!!!
# Allow any settings to be defined in local_settings.py, which should be
# ignored in your version control system, allowing for settings to be
# defined per machine.
try:
    from local_settings import *  # NOQA
except ImportError as e:
    if "local_settings" not in str(e):
        raise e