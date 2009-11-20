import random
from XenAutoMigrate.Base.models import *
from time import sleep
from threading import Thread

class ThreadAutoColetor(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print 'Iniciando coletor'
        while 1:
            allXenHosts = XenHost.objects.all()
            print allXenHosts.count(), u" hosts para buscar informacoes"
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

