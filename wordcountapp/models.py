from django.db import models

# Create your models here.

class FileUpload(models.Model):
	upload_file = models.FileField(upload_to='uploads/')
