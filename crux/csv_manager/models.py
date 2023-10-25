from django.db import models


# Create your models here.

class CSVData(models.Model):
    description = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    document = models.FileField(upload_to='')
    title = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class CSVConfig(models.Model):
    csv_data = models.OneToOneField(CSVData, on_delete=models.CASCADE)
    delimiter = models.CharField(max_length=10, default=',')
    file_config = models.JSONField(default=dict)