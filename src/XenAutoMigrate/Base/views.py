import math
from django.shortcuts import render_to_response
import	openFlashChart
from django.http import HttpResponse
from XenAutoMigrate.Base.models import *
from calendar import *
from	openFlashChart_varieties import (Line,
										 Line_Dot,
										 Line_Hollow,
										 Bar,
										 Bar_Filled,
										 Bar_Glass,
										 Bar_3d,
										 Bar_Sketch,
										 HBar,
										 Bar_Stack,
										 Area_Line,
										 Area_Hollow,
										 Pie,
										 Scatter,
										 Scatter_Line)

from	openFlashChart_varieties import (dot_value,
										 value,
										 bar_value,
										 bar_3d_value,
										 bar_glass_value,
										 bar_sketch_value,
										 bar_stack_value,
										 pie_value,
										 scatter_value,
										 x_axis_labels,
										 x_axis_label)

def index(request):

    chartList = []
    xenHostList = XenHost.objects.all();
    print "Total de ", len(xenHostList), " hosts"
    for xenHost in xenHostList:
        xenHost.chart = openFlashChart.flashHTML('100%', '400', '/monitor/data/' + str(xenHost.id), "http://localhost/")
        chartList.append(xenHost)
    
    return render_to_response('Base/monitor.xhtml', {'chartList': chartList})

def data(request, xen_id):
    from random import randint

    print "chamado para o id", xen_id
    xenHost = XenHost.objects.filter(id=xen_id)[0]

    data = "{ elements : ["

        # Obtem na base estatisticas por host
    querySetByHost = XenHostStatistic.objects.filter(xenHost=xenHost)
    #querySetByHostAndTime = querySetByHost.filter(date__range=(horaLimite, horaAtual))
    virtualMachinesStatistics = querySetByHost.order_by('-date')[:10]
    values = []
    x_max = 0

    data = data + "type: 'line', values: ["
    hora_referencia = timegm(virtualMachinesStatistics[len(virtualMachinesStatistics)-1].date.timetuple())
    for guestStat in virtualMachinesStatistics:
        #vm_guest = VirtualMachine(realMachine=host, vm_id=guestStat['vm_id'], weight=guestStat['cpu_average'])
        y = guestStat.cpu
        x = timegm(guestStat.date.timetuple())-hora_referencia
        values.append(value((y)))
        if x > x_max:
            x_max = x

    data = data + "], title : { text: 'Three lines example' }, y_axis: { min: 0, max: 20, steps: 5 }}"
    plot = Line(colour = '#FFD600', values = values)
    plot.set_dot_size(3)

    chart = openFlashChart.template(str(xenHost.name))
    #chart.set_x_axis(min = 0, max = x_max, steps=x_max/10)
    chart.set_y_axis(min = 0, max = 100, steps=10)
    
    chart.add_element(plot)

    return HttpResponse(chart.encode())


