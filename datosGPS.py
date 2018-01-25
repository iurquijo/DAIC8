import gps
import time
import RPi.GPIO as GPIO
import os
import enviarMail

#INCLINOMETRO Y LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)
GPIO.setup(21, GPIO.OUT)


latitude = 0.00
longitude = 0.00


session = gps.gps("localhost", "2948")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
x = 1

lista_velocidades = [0,1,2,3]
coordenadas = {}
while True:

     report = session.next()
     if report == None:
          break
          print report['class']

     if report['class'] == 'TPV':
	 print '\nIteracion'
	 GPIO.output(21, GPIO.LOW)
         if hasattr(report, 'time'):
             print 'Hora: ' + str(report.time)
         if hasattr(report, 'lat'):
             print 'Latitud: ' + str(report.lat)
             lati = report.lat
         if hasattr(report, 'lon'):
             print 'Longitud: ' + str(report.lon)
	     long = report.lon
        # return coordenadas
         if hasattr(report, 'speed'):
             print 'Velocidad actual: ' + str(report.speed* gps.MPS_TO_KPH) + 'km/h'
             print 'Velocidad anterior: ' + str(lista_velocidades[len(lista_velocidades) - 1 ]) + 'km/h'
             print 'Resta de Velocidades: ' + str(lista_velocidades[len(lista_velocidades) - 1 ] - report.speed* gps.MPS_TO_KPH) + 'km/h'

             if lista_velocidades[len(lista_velocidades) - 1 ] - report.speed* gps.MPS_TO_KPH > 3:
                 print 'FRENAZO'
	       
		 GPIO.output(21, GPIO.HIGH)
		 time.sleep(1)
	         #GPIO.output(21, GPIO.LOW)
	
	     if lista_velocidades[len(lista_velocidades) - 1 ] - report.speed* gps.MPS_TO_KPH >4:
		 print 'ACCIDENTE??'
                 if (GPIO.input(26)==1):
		    print 'HAY ACCIDENTE'
                    #ENVIAR EMAIL
                  
                    enviarMail.sendemail(from_addr    = 'cascointeligente8@gmail.com', 
                 	 to_addr_list = ['iurquijo@opendeusto.es'],
                 	 cc_addr_list = [''],
                 	 subject      = 'Ayuda, he tenido un accidente!', 
                 	 message      = 'Mi ubicacion es %f, %f' % (lati, long),
                 	 login        = 'cascointeligente8@gmail.com', 
                 	 password     = 'cascogrupo8')
                   # email.sendemail(from_addr    = 'cascointeligente8@gmail.com', 
                 #       to_addr_list = ['dcasado@deusto.es'],
                  #      cc_addr_list = [''],
                  #      subject      = 'Ayuda, he tenido un accidente!', 
                 #       message      = 'Mi ubicacion es %f, %f' % (lati, long),
                 #       login        = 'cascointeligente8@gmail.com', 
                 #       password     = 'cascogrupo8')


   		# time.sleep(3)	

             #actualizacion array
             velocidad_previa = report.speed * gps.MPS_TO_KPH
             lista_velocidades.append(velocidad_previa)
         if hasattr(report, 'track'):
             print 'Rumbo: ' + str(report.track)
         if hasattr(report, 'head'):
             print report.head


