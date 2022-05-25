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


webserver_url = 'https://webserver.mosquitoalert.com/'

#############
# USERFIXES #
#############
"""Size of the grid (in degrees).

This value indicates the minimum distance between the points stored in the
table tigaserver_app_fix. Do not change this value unless it has already
changed in that table."""
gridsize = 0.05
