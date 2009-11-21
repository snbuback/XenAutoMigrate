#!/usr/bin/env python
from threading import Timer
from django.core.management import execute_manager
import sys

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

def inicia_coletor():
    print "Iniciando threads"
    from XenAutoMigrate.Base.coletor import ThreadAutoColetor
    from XenAutoMigrate.Base.balancer import ThreadAutoBalancer

    t_coletor = ThreadAutoColetor()
    t_coletor.start()

    t_balancer = ThreadAutoBalancer()
    t_balancer.start()

if __name__ == "__main__":
    # Inicia as threads de colecao e analise do sistema somente se estiver no modo server.
    args = sys.argv[1:]
    if "runserver" in args:
        t = Timer(5, inicia_coletor)
        t.start() # aguarda 5 segundos para iniciar a thread coletor para que o django tenha iniciado

    print "Iniciando DJANGO"
    execute_manager(settings)
    print "Terminando DJANGO"


