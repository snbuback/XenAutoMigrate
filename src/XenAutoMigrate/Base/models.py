from django.db import models

# Create your models here.
class XenHost(models.Model):
    name = models.CharField(max_length=50)
    host = models.CharField(max_length=50)
    port = models.IntegerField()

    def __unicode__(self):
        return "XenHost("+self.name + ", host=" + self.host + ")"



class XenHostStatistic(models.Model):
    xenHost = models.ForeignKey(XenHost)
    cpu = models.IntegerField()
    net = models.IntegerField()
    disk = models.IntegerField()
    vm_id = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return "XenHostStatistic(host=" + str(self.xenHost) +", cpu=" + str(self.cpu) + ", net=" + str(self.net) + ", disk=" + str(self.disk) + ", date=" + str(self.date) + ", vm_id=" + str(self.vm_id) + ")"


