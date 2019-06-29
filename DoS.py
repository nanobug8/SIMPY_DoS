from SimPy.Simulation import *
import random
import threading
import matplotlib.pyplot as plt


procesor=0
threads= list()
requestOnDoS=0
totalR = 0
t=0

class SSLConnection(Process):

    #############################
    # generates random arrivals #
    #############################

    def run(self, N, lamb, mu):
        for i in range(N):
            a = SSLPacket(str(i))
            activate(a, a.newConnection(mu))
            t = random.expovariate(lamb)
            yield hold, self, t

def clientRenegotiation(id, R):
    global t

    while(R>=0):
        G.DoS.observe(t)
        S.cantR += 1
        time =random.uniform(0.045471023, 0.065548125)
        t = time * S.cantR
        R= R-1

        if(t>=120):
            S.cantDoS += 1
        else:
            t -= time * S.cantR


class SSLPacket(Process):
    def __init__(self, id):
        Process.__init__(self)
        self.id=id

    ######################################
    # we model the behavior of an entity #
    ######################################

    def newConnection(self,mu):
        global threadsrequestOnDoS
        yield hold,self, mu
        R = random.randint(0,100)
        x = threading.Thread(target=clientRenegotiation, args=(id, R,))
        threads.append(x)
        x.start()

class G:
    procesor = 'dummy'
    tiempoensistema=Monitor('Tiempo en el sistema')
    clienteHello = Monitor('Envia client from SimPy.Simulation import *Hello de tantos K de tamano')
    ultimoensalir = 0
    DoS=Monitor('Many times server is not responding')

class S:
    cantR = 0
    cantDoS = 0



def model(c, N, lamb, mu,maxtime, rvseed):
    # Initialization of the simulation engine and seed
    # c: number of cores
    # N: number of arrivals to generate for the simulation
    # lamb: arrival rate
    # mu: service rate
    # maxtime: maximum simulation time
    # rvseed: seed for random values

    initialize()
    random.seed(rvseed)
    G.procesor = Resource(c)

    #############################
    #         Execution         #
    #############################

    s = SSLConnection()
    activate(s, s.run(N, lamb,mu))
    simulate(until=maxtime)


acumR = 0
acumDoS = 0

0
iterations=1
for i in range(iterations):
    sem = random.randint(1, 500)
    model(c=1, N=150, lamb=1000, mu=0.01, maxtime=1000,rvseed=sem)

    acumR += S.cantR
    acumDoS += S.cantDoS

    # cleaning vars
    S.cantR = 0
    S.cantDoS = 0


print(" ---------------------------------------------------------------------")
print("#Renegotiations:",acumR/iterations)
print("#Request on DoS:",acumDoS/iterations)
print("mean time DoS: ", G.DoS.mean())
print (" ---------------------------------------------------------------------")

plt.plot(G.DoS.tseries(),G.DoS.yseries())
plt.show()
