from django.db import models


# Create your models here.

class CSVData(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    title = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)
