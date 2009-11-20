from django.db import models

# Create your models here.
class XenHost(models.Model):
    host = models.CharField(max_length=20)

class XenHostStatistics(models.Model):
    xenHost = models.ForeignKey(XenHost)
    cpu = models.IntegerField()
    net = models.IntegerField()
    disk = models.IntegerField()
