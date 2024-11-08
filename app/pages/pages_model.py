from django.db import models
from django.utils import timezone
from ..websites.websites_model import Website

class Page(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scraped', 'Scraped'),
        ('error', 'Error'),
    ]

    web = models.ForeignKey(Website, on_delete=models.CASCADE)
    url = models.URLField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    last_scraped = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'pages'
        verbose_name = 'Page'  # Singular for clarity
        verbose_name_plural = 'Pages'

    def soft_delete(self):
        """Perform a soft delete by setting the deleted_at timestamp."""
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.url
