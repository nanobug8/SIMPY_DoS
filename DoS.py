from SimPy.Simulation import *
import random
import threading

procesor=0
threads= list()

class SSLConnection(Process):
    # genera arribos aleatorios
    def run(self, N, lamb, mu):
        # genera los arribos de N entidades
        for i in range(N):
            a = SSLPacket(str(i))  # str(i) es el identificador de cliente
            activate(a, a.newConnection(mu))
            # calcula el tiempo del próximo arrivo...
            t = random.expovariate(1./lamb)
            # ... y lo planifica para el futuro (tiempo actual de la simulación + t
            yield hold, self, t

def clientRenegotiation(id):
    global procesor
    while(procesor<=100):
        timeout=300/1000

        tiempoarribo = now()

        t = (1. / 605)
        print("R", id)
        # planificamos el fin de servicio
        G.clienteHello.observe(now() - tiempoarribo)

        procesor += 0.8
        print("CPU " ,procesor,"\n")

        # print(now(), "Fin Cliente ", self.id)
        G.tiempoensistema.observe(now() - tiempoarribo)
        G.ultimoensalir = now()
        # yield release, self, G.procesor
        # else:
        # print('El procesador ya no responde  <DoS>' ,self.id)
        if(procesor>=100):
                print("SERVER NOT RESPONDING <DoS>")

class SSLPacket(Process):
    # se implementa init a los efectos de asignar un identif    logging.info("Thread %s: finishing", name)icador a esta instancia de cliente
    def __init__(self, id):
        Process.__init__(self)
        self.id=id

    # modelamos el comportamiento de una entidad
    def newConnection(self,mu):
        global threads
        print (now(), "Inicia Conexion", self.id)
        yield hold,self,  mu
        x=threading.Thread(target=clientRenegotiation, args=(self.id,))
        threads.append(x)
        x.start()


class G:
    procesor = 'dummy'
    tiempoensistema=Monitor('Tiempo en el sistema')
    clienteHello = Monitor('Envia client Hello de tantos K de tamano')
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


# lamb=tiempo entre arribos (media); mu=tiempo de servicio (media)
model(c=4, N=500, lamb=0.5, mu=0.6, maxtime=1000,rvseed=1234)
