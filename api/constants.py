# coding=utf-8
"""Constants accross the application."""
from django.conf import settings

maxReports = 300
maxDownloads = 300
managers_group = 'gestors'
superusers_group = 'supermosquito'
epidemiologist_editor_group = 'epidemiologist'
epidemiologist_viewer_group = 'epidemiologist_viewer'
epidemiologist_group = 'epidemiologist'
irideon_traps_viewer = 'iridion_traps_viewer'

"""
All roles allowed

  - sorted by permissivity (most permissive appears first)
"""
user_roles = [superusers_group, managers_group]


#############
# USERFIXES #
#############
"""Size of the grid (in degrees).

This value indicates the minimum distance between the points stored in the
table tigaserver_app_fix. Do not change this value unless it has already
changed in that table."""
gridsize = 0.05

#############
# DOWNLOADS #
#############

""" Download columns values.

This values are used to determine if some column values should be included 
when downloading"""

site_value = 'site'

###############
# MODELS DATA #
###############

""" Models data location

This values are used to determine where models data is located"""

VECTORS_MODEL_NAMES = ['tig', 'jap']
VECTORS_MODEL_FOLDER = settings.BASE_DIR / 'media/models/vector/'
VECTORS_FILE_NAME = 'model'
VECTORS_FILE_EXTENSION = '.csv'

BITES_MODEL_FOLDER = settings.BASE_DIR / 'media/models/biting/'
BITES_FILE_NAME = 'model'
BITES_FILE_EXTENSION = '.csv'
