from numpy import linspace
import seaborn as sns
import pylab as pl

#request user input for the current
I = float(input('Enter an input current (nA): '))

#initialize properties of the neuron
dt = 0.05 #time increment
sim_time = 30 #simulation time in ms
time = linspace(0, sim_time, num = 1 + (sim_time/dt)) #array of time increments
V = [0] * len(time) #initialized with resting membrane potential of -70 mV
V_thresh = 2 #scaled for now, but threshold potential is typically between -55 and -50mV (Seifter 2005, p. 55) (https://books.google.com/books?id=A8H_9S4E0I4C&pg=PA55#v=onepage&q&f=false)
spike = 11 #voltage of a spike peak
R = 1
C = 10
tau = R*C

#compute membrane potential for each time increment
i = 0
refrac = 3.5 #refractory period in ms, taken from: http://www.physiologyweb.com/lecture_notes/neuronal_action_potential/neuronal_action_potential_refractory_periods.html
rest_until = 0
for t in time:
    if t > rest_until:
        dv = ((-V[i-1]+R*I)/tau)*dt
        V[i] = V[i-1] + dv
        #check for spike condition
    if V[i] >= V_thresh:
        V[i] = spike
        rest_until = t+refrac
    i+=1

#transform to biologically analogous values
for i in range(len(V)):
    V[i] = V[i]*10-70

#plot
sns.set_style("darkgrid")
pl.plot(time, V)
pl.title('LIF Neuron Simulation with Input Current ' + str(I) + 'nA')
pl.xlabel('Simulation Time (ms)')
pl.ylabel('Membrane Potential (mV)')
pl.show()
