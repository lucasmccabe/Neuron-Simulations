#plots the firing rate of a leaky integrate-and-fire neuron as a function of input current

from numpy import linspace
import seaborn as sns
import pylab as pl

#stimulus (current)
I = linspace(0, 40, num = 1 + (40/.05)) #array of current values

#initialize properties of the neuron
dt = 0.01 #time increment
sim_time = 333333 #simulation time in ms
time = linspace(0, sim_time, num = 1 + (sim_time/dt)) #array of time increments
V = [0] * len(time) #initialized with resting membrane potential of -70 mV
V_thresh = 2 #threshold potential is typically between -55 and -50mV (Seifter 2005, p. 55) (https://books.google.com/books?id=A8H_9S4E0I4C&pg=PA55#v=onepage&q&f=false)
spike = 11 #voltage of a spike peak
R = 1
C = 10
tau = R*C

#estimate firing rate by counting spikes
refrac = 3.5 #refractory period in ms, taken from: http://www.physiologyweb.com/lecture_notes/neuronal_action_potential/neuronal_action_potential_refractory_periods.html
F_rate = [0]*len(I)
for j in range(len(I)):
    rest_until = 0
    i = 0
    V = [0]*len(time)  #initialized with resting membrane potential of -70 mV

    #compute membrane potential for each time increment
    for t in time:
        if t > rest_until:
            dv = ((-V[i-1]+R*I[j])/tau)*dt
            V[i] = V[i-1] + dv
            # check for spike condition
        if V[i] >= V_thresh:
            V[i] = spike
            rest_until = t + refrac
        i += 1

    #transform to biologically analogous values
    for i in range(len(V)):
        V[i] = V[i]*10 - 70

    F_rate[j] = (V.count(40)/sim_time)*1000 #firing rate in spikes/second

#plot
sns.set_style("darkgrid")
pl.plot(I, F_rate)
pl.title('LIF Firing Rate vs. Input Current')
pl.xlabel('Input Current (mA)')
pl.ylabel('Firing Rate (Hz)')
pl.show()
