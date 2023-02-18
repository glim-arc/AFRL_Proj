import numpy as np
import json
import matplotlib.pyplot as plt
# Duration,x^0,x^1,x^2,x^3,x^4,x^5,x^6,x^7,y^0,y^1,y^2,y^3,y^4,y^5,y^6,y^7,z^0,z^1,z^2,z^3,z^4,z^5,z^6,z^7,yaw^0,yaw^1,yaw^2,yaw^3,yaw^4,yaw^5,yaw^6,yaw^7

with open('example.json', 'r') as f:
    data = json.load(f)

figure8 = np.array(data['drone1'])

T = figure8[:, 0]
cx = figure8[:, 1:9]
cy = figure8[:, 9:17]
S = np.hstack([0, np.cumsum(T)])
for leg in range(10):
    t = np.linspace(S[leg], S[leg] + T[leg])
    beta = (t - S[leg])
    x_t = 0
    y_t = 0
    for i in range(8):
        x_t += cx[leg][i]*beta**i
        y_t += cy[leg][i]*beta**i
    plt.plot(t, x_t)
    plt.plot(t, y_t)

plt.grid()
plt.show()
