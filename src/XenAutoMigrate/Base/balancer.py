#from XenAutoMigrate.Base.models import *
from XenAutoMigrate.Base.models import *
from time import sleep
from threading import Thread
from datetime import datetime
from datetime import timedelta
from django.db.models import Avg
from XenAutoMigrate.settings import BALANCER_FREQUENCIA
from XenAutoMigrate.Base.xenapi import XenInterface

class RealMachine():
    def __init__(self, xenHost):
        self.xenHost = xenHost
        self.guests = list()

    def weight(self):
        w = 0
        for guest in self.guests:
            w = w + guest.weight
        return int(w)

    def order(self):
        return int(self.weight())

    def __str__(self):
        return u"RealMachine( name=%s, weight=%d, guests=%s )" % (self.xenHost.name, self.weight(), self.guests)

class VirtualMachine():
    def __init__(self, realMachine, vm_id, weight):
        self.realMachine = realMachine
        self.vm_id = vm_id
        self.weight = weight

    def order(self):
        return int(self.weight)

    def __str__(self):
        return "VirtualMachine(real=%s, vm_id=%s, weight=%d" % (self.realMachine.xenHost.name, self.vm_id, self.weight)


def comp_by_order(x,y):
    return int(x.order() - y.order())


class ThreadAutoBalancer(Thread):
    def __init__(self):
        Thread.__init__(self)
	self.setDaemon(True)

    def run(self):
        print "Iniciando balancer"
        while True:
            print "Dormindo por %d s" % BALANCER_FREQUENCIA
            sleep(BALANCER_FREQUENCIA)

            allXenHosts = XenHost.objects.all()

            if len(allXenHosts) <= 1:
                print "Somente um servidor real... nada para fazer"
                continue

            horaAtual = datetime.now()
            horaLimite = horaAtual - timedelta(seconds=BALANCER_FREQUENCIA)
            print "Obtendo estatisticas entre ", horaLimite, " e ", horaAtual

            vm_hosts = list()

            # Obtem todas as estatisticas do intervalo e calcula a media
            for xenHost in allXenHosts:
                host = RealMachine(xenHost=xenHost)

                # Obtem na base estatisticas por host
                querySetByHost = XenHostStatistic.objects.filter(xenHost=xenHost)
                querySetByHostAndTime = querySetByHost.filter(date__range=(horaLimite, horaAtual))
                virtualMachinesStatistics = querySetByHostAndTime.values('vm_id').annotate(cpu_average=Avg('cpu'), net_average=Avg('net'), disk_average=Avg('disk'))
                for guestStat in virtualMachinesStatistics:
                    vm_guest = VirtualMachine(realMachine=host, vm_id=guestStat['vm_id'], weight=guestStat['cpu_average'])
                    host.guests.append(vm_guest)
                vm_hosts.append(host)

            print "Olha o que foi calculado: ", [ str(x) for x in vm_hosts]

            numeroMaquinasReais = len(vm_hosts)
            total_weight = 0
            for vm in vm_hosts:
                total_weight = total_weight + vm.weight()
            medium_weight = total_weight / numeroMaquinasReais
            print "peso total = %d, peso medio = %d" % (total_weight, medium_weight)

            while True:
                vm_hosts.sort(cmp=comp_by_order, reverse=True)
                vm_host_maior_peso = vm_hosts[0]
                print "Host de maior peso = ", vm_host_maior_peso

                vm_host_menor_peso = vm_hosts[len(vm_hosts)-1]
                print "Host de menor peso = ", vm_host_menor_peso

                migrou = False

                vm_host_maior_peso.guests.sort(cmp=comp_by_order, reverse=True)
                for vm in vm_host_maior_peso.guests:
                    if vm_host_menor_peso.weight() + vm.weight <= medium_weight and vm.weight > 10:

                        print "\n\n\n************\nMigrate vm ", str(vm), " to ", str(vm_host_menor_peso), "\n\n\n\n"

                        xen = XenInterface(host=vm.realMachine.xenHost.host, port=vm.realMachine.xenHost.port)
                        xen.migrate_vm_fvm(vm.vm_id, vm_host_menor_peso.xenHost.host)

                        vm_host_menor_peso.guests.append(vm)
                        vm.realMachine.guests.remove(vm)
                        vm.realMachine = vm_host_menor_peso

                        migrou = True
                        break

                if not migrou:
                    break
            print "Olha como ficou: ", [ str(x) for x in vm_hosts]
        print "\n\n\n*********************Morrendo\n\n"

