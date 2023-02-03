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

#################
# PUBLIC FIELDS #
#################

private_fields = [ 'note' ]
public_fields = [
  'id', 'version_uuid', 'user_id', 'observation_date', 'lon', 'lat', 'ref_system', 'type', 'expert_validated', 'expert_validation_result', 
  'simplified_expert_validation_result', 'site_cat', 'storm_drain_status', 'edited_user_notes', 'photo_url', 'photo_license', 'dataset_license', 
  'single_report_map_url', 'private_webmap_layer', 'final_expert_status', 'tags', 'breeding_site_answers', 'mosquito_answers', 
  'n_photos', 'visible', 'responses_json', 'report_id', 'nuts3_code', 'nuts3_name', 'bite_location', 'validation', 
  'ia_value', 'larvae', 'bite_count', 'bite_time', 'lau_code', 'lau_name', 'nuts0_code', 'nuts0_name'
]

private_layers = [ 'not_yet_validated', 'breeding_site_not_yet_filtered' ]
public_layers = [
  'mosquito_tiger_confirmed', 'albopictus_cretinus', 'yellow_fever_probable', 'yellow_fever_confirmed',
  'japonicus_probable', 'japonicus_confirmed', 'japonicus_koreicus',
  'koreicus_probable', 'koreicus_confirmed', 'japonicus_koreicus',
  'culex_probable', 'culex_confirmed','unidentified', 'other_species','bite',
  'storm_drain_water','storm_drain_dry','breeding_site_other'  
]

private_download_fields = ['report_id', 'note']
public_download_fields =[
  'version_uuid', 'report_id', 'observation_date', 'lon', 'lat',
  'ref_system', 'nuts0_code', 'nuts0_name', 'nuts3_code', 'nuts3_name',
  'lau_code', 'lau_name', 'type', 'expert_validated', 'private_webmap_layer',
  'ia_value', 'larvae', 'bite_count', 'bite_location',
  'bite_time', 'map_link'
]
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

This is the value of the column 'type' in MapAuxReport model for mosquito reproduction sites
"""

site_value = 'site'

#################################
# CORS.  ACCEPT CALLS ONLY FROM #
#################################

allowed_referers = [
  # This referers must be contained in request header referer
  'http://localhost:8080',
  'https://sigserver4.udg.edu/mos/spa'
  ]