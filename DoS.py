from SimPy.Simulation import *
import random

class SSLConnection(Process):
    # genera arribos aleatorios
    def run(self, N, lamb, mu):
        # genera los arribos de N entidades
        for i in range(N):
            a = SSLPacket(str(i))  # str(i) es el identificador de cliente
            activate(a, a.run(mu))
            # calcula el tiempo del próximo arrivo...
            t = random.expovariate(1./lamb)
            # ... y lo planifica para el futuro (tiempo actual de la simulación + t
            yield hold, self, t

class SSLPacket(Process):
    # se implementa init a los efectos de asignar un identificador a esta instancia de cliente
    def __init__(self, id):
        Process.__init__(self)
        self.id=id

    # modelamos el comportamiento de una entidad
    def run(self, mu):
        print (now(), "Inicia Conexion", self.id)
        timeout=300/1000
        tiempoarribo=now()
        # intenta tomar el recurso G.server
        yield (request, self, G.procesor), (hold,self, timeout)
        if self.acquired(G.procesor):
           #G.tiempoencola.observe(now()-tiempoarribo)
            # en este punto el server ya fue asignado a la entidad
            t = random.expovariate(1./mu)/1000
            print (now(), "Conexion", self.id, " comienza a interactuar con el server (tiempo servicio: ",t,")")
            # planificamos el fin de servicio
            G.clienteHello.observe(now() - tiempoarribo)
            yield hold, self, t
            #G.tiempoutilizacion.observe(t)
            # en este punto el servicio ya fue ejecutado, resta liberar el server
            yield release, self, G.procesor
            print (now(), "Fin Cliente ", self.id)
            G.tiempoensistema.observe(now()-tiempoarribo)
            G.ultimoensalir=now()
        else:
            print('El procesador ya no responde  <DoS>')

class G:
    procesor = 'dummy'
    tiempoensistema=Monitor('Tiempo en el sistema')
    clienteHello = Monitor('Envia client Hello de tantos K de tamano')
    #tiempoencola=Monitor('Tiempo en cola')
    #tiempoutilizacion=Monitor('Tiempo de utilización del servidor')
    #clientesencola=Monitor('Clientes en cola','Clientes', 't')
    ultimoensalir=0


def model(c, N, lamb, mu, maxtime, rvseed):
    # inicialización del motor de simulación y semilla
    initialize()
    random.seed(rvseed)
    # definimos el recurso G.server con "c" unidades (será un parámetro de la simulación)
    G.procesor = Resource(c)
    #  ejecución
    s = SSLConnection()
    activate(s, s.run(N, lamb, mu))
    simulate(until=maxtime)
    print ("Tiempo promedio en sistema: ", G.tiempoensistema.mean())
   # print ("Tiempo promedio en cola: ", G.tiempoencola.mean())
    #print ("Tasa utilización servidor: ", G.tiempoutilizacion.total()/G.ultimoensalir)
    # ejemplo de uso de histograma
    print (G.tiempoensistema.histogram(low=0.0,high=max(G.tiempoensistema.yseries()),nbins=4))

   # print ("Cantidad de clientes promedio en la cola: ", G.clientesencola.timeAverage(G.ultimoensalir))

# Experimento
# lamb=tiempo entre arribos (media); mu=tiempo de servicio (media)
model(c=1, N=100, lamb=2, mu=10, maxtime=100000,rvseed=1234)