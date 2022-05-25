from django.db import models
import uuid

# Create your models here.
class ProvinceManager(models.Manager):
    """Province manager. Ordering."""

    def get_queryset(self):
        """Just ordering province name."""
        return super(ProvinceManager, self).get_queryset().order_by('name')


class Province(models.Model):
    """Provinces."""

    id = models.CharField(primary_key=True, max_length=2)
    nomprov = models.CharField(max_length=255, null=False)

    def get_queryset(self):
        """"get_queryset."""
        return super(Province, self).order_by('nomprov')

    def __str__(self):
        """Convert the object into a string."""
        return self.nomprov

    class Meta:
        """Meta."""

        db_table = 'provincies_4326'


class MunicipalitiesManager(models.Manager):
    """Municipalities manager."""

    def get_queryset(self):
        """"get_queryset."""
        return super(MunicipalitiesManager, self).get_queryset().filter(
            tipo='Municipio'
        ).order_by('codprov', 'nombre')


class Municipality(models.Model):
    """Municipalities."""

    gid = models.AutoField(primary_key=True)
    municipality_id = models.IntegerField(unique=True, null=True)
    nombre = models.CharField(max_length=254, blank=True)
    tipo = models.CharField(max_length=10, blank=True)
    pertenenci = models.CharField(max_length=50, blank=True, null=True)
    codigoine = models.CharField(max_length=20, blank=True)
    codprov = models.ForeignKey(Province, db_column='codprov', null=True,
                                on_delete=models.CASCADE)
    cod_ccaa = models.CharField(max_length=2, blank=True, null=True)

    # objects = MunicipalitiesManager()

    def __str__(self):
        """Convert the object into a string."""
        return self.nombre + ' (' + self.codprov.nomprov + ')'

    class Meta:
        """Meta."""

        db_table = 'municipis_4326'


class MapAuxReport(models.Model):
    """All mosquito observations."""
        
    id = models.IntegerField(primary_key=True)
    version_uuid = models.CharField(max_length=36, blank=True, unique=True)
    user_id = models.CharField(max_length=36, blank=True)
    observation_date = models.DateTimeField(null=True, blank=True)
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    ref_system = models.CharField(max_length=36, blank=True)
    type = models.CharField(max_length=7, blank=True)

    expert_validated = models.BooleanField(null=True)    
    expert_validation_result = models.CharField(max_length=100, blank=True)
    simplified_expert_validation_result = models.CharField(max_length=100,
                                                           blank=True)
    site_cat = models.IntegerField(blank=True, null=True)
    storm_drain_status = models.CharField(max_length=50, blank=True)
    edited_user_notes = models.CharField(max_length=4000, blank=True)
    photo_url = models.CharField(max_length=255, blank=True)
    photo_license = models.CharField(max_length=100, blank=True, null=True)
    dataset_license = models.CharField(max_length=100, blank=True, null=True)
    single_report_map_url = models.CharField(max_length=255, blank=True)
    private_webmap_layer = models.CharField(max_length=255, blank=True,  null=True)
    final_expert_status = models.IntegerField()
    note = models.TextField()
    tags = models.TextField(null=True)

    breeding_site_answers = models.CharField(max_length=100, blank=True)
    mosquito_answers = models.CharField(max_length=100, blank=True)
    n_photos = models.IntegerField(blank=True, null=True)
    visible = models.BooleanField()
    responses_json = models.TextField(blank=True, null=True)
    report_id = models.CharField(max_length=10, blank=True, null=True)

    nuts3_code = models.CharField(max_length=5, default=None, null=True)
    nuts3_name = models.CharField(max_length=155, default=None, null=True)
    bite_location = models.CharField(max_length=100, null=True, default=None)
    validation = models.IntegerField(default=None, null=True)
    ia_value = models.FloatField(default=None, null=True)
    larvae = models.BooleanField(default=None, null=True)
    bite_count = models.IntegerField(blank=True, default=None, null=True)
    
    t_q_1 = models.CharField(max_length=255, default=None, null=True)
    t_q_2 = models.CharField(max_length=255, default=None, null=True)
    t_q_3 = models.CharField(max_length=255, default=None, null=True)
    t_a_1 = models.CharField(max_length=255, default=None, null=True)
    t_a_2 = models.CharField(max_length=255, default=None, null=True)
    t_a_3 = models.CharField(max_length=255, default=None, null=True)
    s_q_1 = models.CharField(max_length=255, default=None, null=True)
    s_q_2 = models.CharField(max_length=255, default=None, null=True)
    s_q_3 = models.CharField(max_length=255, default=None, null=True)
    s_q_4 = models.CharField(max_length=255, default=None, null=True)
    s_a_1 = models.CharField(max_length=255, default=None, null=True)
    s_a_2 = models.CharField(max_length=255, default=None, null=True)
    s_a_3 = models.CharField(max_length=255, default=None, null=True)
    s_a_4 = models.CharField(max_length=255, default=None, null=True)

    def save(self, *args, **kwargs):
        self.tags = self.tags.lower()
        return super(MapAuxReport, self).save(*args, **kwargs)

    class Meta:
        """Meta."""

        db_table = 'map_aux_reports'


class Userfixes(models.Model):
    """Userfixes model."""

    id = models.IntegerField(primary_key=True)
    fix_time = models.DateTimeField(blank=True, null=True)
    server_upload_time = models.DateTimeField(blank=True, null=True)
    phone_upload_time = models.DateTimeField(blank=True, null=True)
    masked_lon = models.FloatField(blank=True, null=True)
    masked_lat = models.FloatField(blank=True, null=True)
    mask_size = models.FloatField(blank=True, null=True)
    power = models.FloatField(blank=True, null=True)
    user_coverage_uuid = models.CharField(max_length=36, blank=True, null=True)

    def _get_the_type(self):
        """a."""
        return 'Feature'

    thetype = property(_get_the_type)

    class Meta:
        """Meta information."""

        db_table = 'tigaserver_app_fix'


class MapView(models.Model):
    """MapView model."""
    code=models.CharField(max_length=6, null=False, blank=False, unique=True)    
    view = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

class ReportView(models.Model):
    """MapView model."""
    code=models.CharField(max_length=8, null=False, blank=False, unique=True)    
    view = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)    