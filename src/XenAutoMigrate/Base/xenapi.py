from xen.xm.XenAPI import Session

class XenData():
    def __init__(self, uuid, cpu):
        self.uuid = uuid;
        self.cpu = cpu

class XenInterface():
    def __init__(self, host, port):
        self.session = Session("http://%s:%d" % (host, port))
        self.session.login_with_password('', '')
        print "Session: " + str(self.session)

    # Retorna uma lista de XenData para cada VM da maquina fisica
    def get_data_vms(self):
        vm = self.session.xenapi.VM
        vm_list = self.session.xenapi.VM.get_all()
        print vm_list

        vm_list = vm_list[1:]
        
        list_vm_data = []

        for vm_ref in vm_list:
            vm_metrics = self.session.xenapi.VM.get_metrics(vm_ref)
            cpu_carga =  self.session.xenapi.VM_metrics.get_VCPUs_utilisation(vm_metrics)
            #print "******** cpu carga", cpu_carga
            vcpus = self.session.xenapi.VM_metrics.get_VCPUs_CPU(vm_metrics)
            # Obtem qual o processador da vcpu0 para fazer normalizacao ao final
            vcpu0 = vcpus['0']
            vm_instance = XenData(uuid=vm_ref,cpu=round(cpu_carga['0']*100))
            vm_instance.vcpu = vcpu0
            #vm_instance = XenData(uuid=100,cpu=255)
            list_vm_data.append(vm_instance)

	# faz normalizacao das cpus
	consolidacao_por_cpu = {}
        for item in list_vm_data:
            print "Antes normalizacao", item.uuid, item.cpu, item.vcpu
            if item.vcpu not in consolidacao_por_cpu:
               consolidacao_por_cpu[item.vcpu] = { 'sum': 0, 'max' : 0 }
            c = consolidacao_por_cpu[item.vcpu]
            c['sum'] = c['sum'] + item.cpu
            c['max'] = (item.cpu if c['max'] < item.cpu else c['max'])

        # normalizando
        for item in list_vm_data:
            if consolidacao_por_cpu[item.vcpu]['max'] > 0:
               item.cpu = round(item.cpu/consolidacao_por_cpu[item.vcpu]['max']*consolidacao_por_cpu[item.vcpu]['sum'])
            print "Apos normalizacao", item.uuid, item.cpu, item.vcpu
        

        return list_vm_data

    # Migra(LIVE) de uma maquina virtual a partir de seu UUID para uma maquina fisica
    # sudo xm migrate 7a2232de-5c5b-ae98-80e1-eeee6e1686fa 192.168.2.20 --live
    def migrate_vm_fvm(self,uuid,ip_host):
        print "Migrate started: "
        vm_migrate_data = self.session.xenapi.VM.migrate(uuid,ip_host,'true',{'':''})
        print "Migrate finish: ", vm_migrate_data
        
