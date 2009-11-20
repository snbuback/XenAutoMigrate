from django.db import models

# Create your models here.
class XenHost(models.Model):
    host = models.CharField(max_length=20)

    def __unicode__(self):
        return "XenHost("+self.host+")"



class XenHostStatistic(models.Model):
    xenHost = models.ForeignKey(XenHost)
    cpu = models.IntegerField()
    net = models.IntegerField()
    disk = models.IntegerField()

    def __unicode__(self):
        return "XenHostStatistic(host=" + self.xenHost.__str__() +", cpu=" + self.cpu.__str__() + "net=" + self.net.__str__() + "disk=" + self.disk.__str__() + ")"


