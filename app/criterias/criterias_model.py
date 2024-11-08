from django.db import models
from ..websites.websites_model import Website

class Criterias(models.Model):
    NAV = 'nav'
    CONTENT = 'content'
    
    TYPE_CHOICES = [
        (NAV, 'Navigation'),
        (CONTENT, 'Content'),
    ]
    
    id = models.AutoField(primary_key=True)
    html_tag = models.CharField(max_length=50)
    css_selector = models.CharField(max_length=255)
    meta = models.JSONField(blank=True, null=True)
    
    # Adding the `type` field with enum choices
    type = models.CharField(
        max_length=7,  # 'nav' or 'content'
        choices=TYPE_CHOICES,
        default=CONTENT,
    )
    
    web_id = models.ForeignKey(
        Website,
        on_delete=models.CASCADE,
        related_name='criterias',
        null=True,
        blank=True,
        db_column='web_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'criterias'
        verbose_name = 'Criteria'
        verbose_name_plural = 'Criterias'

    def __str__(self):
        return f"{self.html_tag} - {self.type}"
