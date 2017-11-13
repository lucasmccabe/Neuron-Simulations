#simulates a Hodgkin-Huxley neuron with the drug TTX inhibiting sodium current

from numpy import linspace, exp
import seaborn as sns
import pylab as pl

#request user input for the current
I = float(input('Enter an input current (nA): '))

#initialize properties of the neuron
dt = 0.05 #time increment
sim_time = 30 #simulation time in ms
time = linspace(0, sim_time, num = 1 + (sim_time/dt)) #time array

#Values given by Table 3 of the Hodgkins-Huxley paper
C = 1
g_k = 36 #potassium conductance in mS/cm^2
g_n = 120 #sodium conductance in mS/cm^2
gl = 0.3 #leak conductance in mS/cm^2
Vk = -12 #potassium potential in mV
Vn = 115 #sodium potential in mV
Vl = 10.613 #leak potential in mV

#useful functions
def alpha_n(x):
    return 0.01*(-x+10)/(exp((-x+10)/10)-1)

def beta_n(x):
    return 0.125*exp(-x/80)

def alpha_m(x):
    return 0

def beta_m(x):
    return 0

def alpha_h(x):
    return 0.07*exp(-x/20)

def beta_h(x):
    return 1/(exp((-x+30)/10)+1)

def d_n(n, v):
    return (alpha_n(v)*(1 - n) - beta_n(v)*n)*dt

def d_m(m, v):
    return (alpha_m(v)*(1 - m) - beta_m(v)*m)*dt

def d_h(h, v):
    return (alpha_h(v)*(1 - h) - beta_h(v)*h)*dt

#initialize
V = [0]*len(time)
n = alpha_n(0)/(alpha_n(0) + beta_n(0))
m = 0
h = alpha_h(0)/(alpha_h(0) + beta_h(0))

#compute membrane potential for each time increment
for i in range(len(time)):
    gn = g_n*(m**3)*h
    gk = g_k*(n**4)

    dn = d_n(n, V[i-1])
    n += dn

    dm = d_m(m, V[i-1])
    m += dm

    dh = d_h(h, V[i-1])
    h += dh

    dv = (1/C)*(I - gn * (V[i - 1] - Vn) - gk * (V[i - 1] - Vk) - gl * (V[i - 1] - Vl))*dt
    V[i] = V[i-1] + dv

#transform to biologically analogous values
for i in range(len(V)):
    V[i] = V[i]-70

#plot
sns.set_style("darkgrid")
pl.plot(time, V)
pl.title('Hodgkin-Huxley Neuron Simulation Response to Drug TTX with Input Current ' + str(I) + 'nA')
pl.xlabel('Simulation Time (ms)')
pl.ylabel('Membrane Potential (mV)')
pl.ylim([-90, 40])
pl.show()
