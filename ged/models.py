from django.db import models
from django.contrib.auth.models import User
from os import path


class Document(models.Model):
    name = models.CharField(max_length = 200)
    genre = models.CharField(max_length = 100)
    user = models.ForeignKey(User)
    scanning_date = models.DateTimeField()

    def __unicode__(self):
        return "%s (document)" % self.name

class Page(models.Model):
    file_name = models.CharField(max_length = 250)
    ocr = models.TextField(blank = True, null = True)
    barcodes = models.TextField(blank = True, null = True)
    document = models.ForeignKey(Document)
    file_web = lambda x: path.basename(x.file_name)

    def __unicode__(self):
        return "%s (page)" % self.document.name


