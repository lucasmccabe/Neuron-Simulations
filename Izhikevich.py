from numpy import linspace
import seaborn as sns
import pylab as pl

#request user input for the current
I = float(input('Enter an input current (nA): '))

#initialize properties of the neuron
dt = 0.05 #time increment
sim_time = 30 #simulation time in ms
time = linspace(0, sim_time, num = 1 + (sim_time/dt)) #array of time increments
V = [-65]*len(time)
U = [-15]*len(time)
V_thresh = -40
spike = 30

#compute membrane potential for each time increment
i = 0
a = 0.02
b = 0.2
refrac = 3.5 #refractory period in ms, taken from: http://www.physiologyweb.com/lecture_notes/neuronal_action_potential/neuronal_action_potential_refractory_periods.html
rest_until = 0
for i in range(len(time)):
    if V[i-1] >= V_thresh:
        du = (a*(b*V[i-1]-U[i-1]))*dt
        U[i] = U[i - 1] + du
        V[i] = -65
        continue
    if V[i] < V_thresh:
        du = (a*(b*V[i-1] - U[i-1]))*dt
        U[i] = U[i-1] + du
        dv = (0.04*((V[i-1])**2) + 5*V[i-1] + 140 - U[i-1] + I)*dt
        V[i] = V[i-1] + dv
    if V[i] >= V_thresh:
        V[i] = spike

#plot
sns.set_style("darkgrid")
pl.plot(time, V)
pl.title('Izhikevich Neuron Simulation with Input Current ' + str(I) + 'nA')
pl.xlabel('Simulation Time (ms)')
pl.ylabel('Membrane Potential (mV)')
pl.ylim([-80, 30])
pl.show()
