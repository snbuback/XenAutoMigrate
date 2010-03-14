import random
from XenAutoMigrate.Base.models import *
from time import sleep
from threading import Thread
from XenAutoMigrate.Base.xenapi import *

class ThreadAutoColetor(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print 'Iniciando coletor'
        while 1:
            allXenHosts = XenHost.objects.all()
            print allXenHosts.count(), "hosts para buscar informacoes"
            for xenHost in allXenHosts:
                print "Pesquisando no host ", xenHost.host
                xenInterface = XenInterface(xenHost.host, xenHost.port)
                vm_data = xenInterface.get_data_vms()
		print "***********", vm_data

                for vm in vm_data:
                    print "###############", vm
                    # faz chamada na xen api
                    cpu = vm.cpu
                    uuid = vm.uuid
                    net = 0
                    disk = 0

                    xenStatistic = XenHostStatistic(xenHost=xenHost, cpu=cpu, net=net, disk=disk, vm_id=uuid)
                    print "Armazenando estatistica: ", xenStatistic
                    xenStatistic.save()

            sleep(10)

