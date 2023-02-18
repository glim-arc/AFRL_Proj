import matplotlib.pyplot as plt

import numpy as np

data = np.loadtxt("data.txt")

t = data[:,0]
m1 = data[:,1]
m2 = data[:,2]
m3 = data[:,3]
m4 = data[:,4]
z = data[:,5]
m = m1+m2+m3+m4
m_norm = m/np.max(m)

plt.figure(1)
plt.plot(t, z, label = 'z')
plt.figure(2)
plt.plot(t, m, label = 'm')
plt.show()

