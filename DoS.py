from SimPy.Simulation import *
import random
import threading
import matplotlib.pyplot as plt

threads = list()
t = 0.00000001

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
    G.DoS.observe(t)
    while R >= 0:
        S.cantR += 1
        time = random.uniform(0.045471023, 0.0605548125) # in seconds
        t = time * S.cantR
        R = R-1

        if t >= 120:
            G.DoS.observe(t)
            S.cantDoS += 1

        else:
            G.success.observe(t)
            t -= time * S.cantR
            S.OK_200 += 1

class SSLPacket(Process):
    def __init__(self, id):
        Process.__init__(self)
        self.id=id

    ######################################
    # we model the behavior of an entity #
    ######################################

    def newConnection(self, mu):
        global threads
        yield hold,self, mu
        R = random.randint(1000,2000)
        x = threading.Thread(target=clientRenegotiation, args=(id, R,))
        threads.append(x)
        x.start()

class G:
    DoS = Monitor('Many times server is not responding')
    success = Monitor('Count 200 OK responses')

class S:
    cantR = 0
    cantDoS = 0
    OK_200 = 0


def model(N, lamb, mu, maxtime, rvseed):
    # Initialization of the simulation engine and seed
    # N: number of arrivals to generate for the simulation
    # lamb: arrival rate
    # mu: service rate
    # maxtime: maximum simulation time
    # rvseed: seed for random values

    initialize()
    random.seed(rvseed)

    #############################
    #         Execution         #
    #############################

    s = SSLConnection()
    activate(s, s.run(N, lamb, mu))
    simulate(until=maxtime)


acumR = 0
acumDoS = 0
acum200OK = 0

iterations = 1000
for i in range(iterations):
    sem = random.randint(1, 500)
    model(N=10, lamb=1000, mu=0.01, maxtime=1000, rvseed=sem)
    acumR += S.cantR
    acumDoS += S.cantDoS
    acum200OK += S.OK_200

    # cleaning vars
    S.cantR = 0
    S.cantDoS = 0
    S.OK_200 = 0


print(" ---------------------------------------------------------------------")
print("Renegotiations:",acumR)
print("Request on DoS:",acumDoS)
print('Success requests: ', acum200OK)
print (" ---------------------------------------------------------------------")


labels = 'DoS time', 'Operative time'
sizes = [G.DoS.count()-1, G.success.count()]
explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

