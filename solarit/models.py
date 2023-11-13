from django.db import models
import os

# Create your models here.
class Solarit_Docs(models.Model):
    title = models.CharField(max_length=200, default=False, blank=True)
    txt_documents = models.FileField(upload_to='txt_documents/', blank=True, default=False)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        # Delete the file from the file system when the object is deleted
        if self.txt_documents:
            if os.path.isfile(self.txt_documents.path):
                os.remove(self.txt_documents.path)
        super().delete(*args, **kwargs)


class Template(models.Model):
    template = models.CharField(max_length=10000, blank=True)
    
    def __str__(self):
        return self.template