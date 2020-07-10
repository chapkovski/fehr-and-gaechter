import os
from os import environ

EXTENSION_APPS = ['pggfg']

# don't share this with anybody.
SECRET_KEY = 'ea_h#&kz!etxef1fikaehvncnk+#y13p##*x80-te1v)_%k#c4'

# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'
ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.000,
    'participation_fee': 0.00,
    'doc': "",
    'use_browser_bots': False
}

SESSION_CONFIGS = [
    {
        'name': 'pggfg',
        'display_name': 'Public Good Game with Punishment (Fehr and Gaechter)',
        'num_demo_participants': 3,
        'app_sequence': ['pggfg'],

    },
]
