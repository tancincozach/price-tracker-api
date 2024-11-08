from django.db import models
from django.utils import timezone

ELKUBEMA = 'elkubema'
KABELBINDER = 'kabelbinder'
class Website(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    base_url = models.URLField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'websites'
        verbose_name = 'Website'
        verbose_name_plural = 'Websites'

    def __str__(self):
        return self.name
