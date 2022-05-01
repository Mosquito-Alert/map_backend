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


####################
# EXPORT EXCEL/CSV #
####################

"""
All fields available.

Each field is a tuple. For each tuple:
  - The first element is the name of the DB column (string)
  - The second element is the name of the Excel/CSV column (string)

Except for the fields restricted to specific roles, in such case:
  - The first element remains the same.
  - The second element is a dict with these attributes:
      - label (string): the name of the Excel/CSV column
      - permissions (list): the roles allowed to see this field
"""
fields_available = [
    ('version_uuid', 'ID'),
    ('user_id', {
        'label': '(PRIVATE COLUMN!!) User',
        'permissions':  [superusers_group, managers_group]
    }),
    ('observation_date', 'Date'),
    ('lon', 'Longitude'),
    ('lat', 'Latitude'),
    ('ref_system', 'Ref. System'),
    ('municipality__nombre', 'Municipality'),
    ('type', 'Type'),
    ('expert_validated', 'Expert validated'),
    ('private_webmap_layer', 'Expert validation result'),
    ('single_report_map_url', 'Map link'),
    ('note', {
         'label': '(PRIVATE COLUMN!!) Tags',
         'permissions': [superusers_group]
    })
]

#############
# USERFIXES #
#############
"""Size of the grid (in degrees).

This value indicates the minimum distance between the points stored in the
table tigaserver_app_fix. Do not change this value unless it has already
changed in that table."""
gridsize = 0.05
