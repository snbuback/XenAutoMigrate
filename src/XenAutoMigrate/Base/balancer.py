#from XenAutoMigrate.Base.models import *
from time import sleep
from threading import Thread

class ThreadAutoBalancer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        print "Iniciando"
        while (True):
            print "Dormindo por 30s"
            sleep(30)




