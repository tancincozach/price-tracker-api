from django.db import models
from django.utils import timezone
from ..pages.pages_model import Page

class ScrapedData(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    field_name = models.TextField()
    field_value = models.TextField()
    field_value_meta = models.TextField() # json values
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        """Sets the deleted_at timestamp to mark the data as deleted without removing it from the database."""
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        db_table = 'scraped_data'
        verbose_name = 'Scraped Data'
        verbose_name_plural = 'Scraped Data'

    def __str__(self):
        return f"{self.field_name}: {self.field_value}"
