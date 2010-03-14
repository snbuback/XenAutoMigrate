

select * from DESENV_CAD.XEN_TESTS where qtd = 0

-- por maquina
select * from DESENV_CAD.XEN_TESTS where vm = 1 order by horaunix;

-- total/por minuto todas as maquinas
select count(1), sum(x.QTD), to_char(x.HORA, 'hh24:mi') from DESENV_CAD.XEN_TESTS x
group by to_char(x.HORA, 'hh24:mi')
order by 3

-- total/por minuto maquina a maquina
select t.hora,
    (select nvl(sum(m1.qtd),0) from xen_tests m1 where m1.vm=1 and t.HORA = to_char(m1.HORA, 'hh24:mi')) as vm1,
    (select nvl(sum(m2.qtd),0) from xen_tests m2 where m2.vm=2 and t.HORA = to_char(m2.HORA, 'hh24:mi')) as vm2,
    (select nvl(sum(m3.qtd),0) from xen_tests m3 where m3.vm=3 and t.HORA = to_char(m3.HORA, 'hh24:mi')) as vm3,
    (select nvl(sum(m4.qtd),0) from xen_tests m4 where m4.vm=4 and t.HORA = to_char(m4.HORA, 'hh24:mi')) as vm4,
    (select nvl(sum(m5.qtd),0) from xen_tests m5 where m5.vm=5 and t.HORA = to_char(m5.HORA, 'hh24:mi')) as vm5
from (
    select to_char(x.HORA, 'hh24:mi') hora
    from XEN_TESTS x
    group by to_char(x.HORA, 'hh24:mi')
    order by 1
) t
order by 1


-- total/por segundo maquina a maquina
select t.hora,
    (select sum(m1.qtd) from xen_tests m1 where m1.vm=1 and t.HORA = to_char(m1.HORA, 'hh24:mi:ss')) as vm1,
    (select sum(m2.qtd) from xen_tests m2 where m2.vm=2 and t.HORA = to_char(m2.HORA, 'hh24:mi:ss')) as vm2,
    (select sum(m3.qtd) from xen_tests m3 where m3.vm=3 and t.HORA = to_char(m3.HORA, 'hh24:mi:ss')) as vm3,
    (select sum(m4.qtd) from xen_tests m4 where m4.vm=4 and t.HORA = to_char(m4.HORA, 'hh24:mi:ss')) as vm4,
    (select sum(m5.qtd) from xen_tests m5 where m5.vm=5 and t.HORA = to_char(m5.HORA, 'hh24:mi:ss')) as vm5
from (
    select to_char(x.HORA, 'hh24:mi:ss') hora
    from XEN_TESTS x
    group by to_char(x.HORA, 'hh24:mi:ss')
    order by 1
) t
order by 1

--                                                                          1268595229

select sysdate-1 from dual

SELECT new_time( to_date('01011970','ddmmyyyy') + 1/24/60/60 * (1268592301319369000/1000000000), 
        'GMT', 'EDT' )
        from dual; 

update DESENV_CAD.XEN_TESTS x set x.HORA = new_time( to_date('01011970','ddmmyyyy') + 1/24/60/60 * (x.HORAUNIX/1000000000), 
        'GMT', 'EDT' )

select tzname,tzabbrev 
       from V$TIMEZONE_NAMES 
      where tzabbrev = 'MST'



