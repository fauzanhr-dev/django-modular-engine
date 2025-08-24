from django.db import models


class Module(models.Model):
    key = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    installed_version = models.CharField(max_length=50, blank=True, null=True)
    landing_url_name = models.CharField(max_length=100, blank=True, null=True)
    is_installed = models.BooleanField(default=False)
    installed_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key} ({'installed' if self.is_installed else 'not installed'})"

    class Meta:
        ordering = ['key']


    