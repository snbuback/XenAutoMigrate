import random
from XenAutoMigrate.coletor.models import XenHost
from XenAutoMigrate.coletor.models import XenHostStatistic
from time import sleep
from threading import Thread
from XenAutoMigrate.coletor.models import *

class ThreadAutoColetor(Thread):
    def __init__ (self):
        Thread.__init__(self)
        self.setDaemon(True)
        print 'Iniciando thread'

    def run(self):
        allXenHosts = XenHost.objects.all()
        print allXenHosts.count(), u" hosts para buscar informacoes"
        while 1:
            for xenHost in allXenHosts:
                print "Pesquisando no host ", xenHost.host
                # faz chamada na xen api
                cpu = random.randint(0, 100)
                net = random.randint(0, 100)
                disk = random.randint(0, 100)
                xenStatistic = XenHostStatistic(xenHost=xenHost, cpu=cpu, net=net, disk=disk)
                print "Armazenando estatistica: ", xenStatistic
                xenStatistic.save()

            sleep(10)

