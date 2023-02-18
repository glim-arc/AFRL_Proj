
#%%
import sys
import os
sys.path.insert(0, os.getcwd())

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np
import bswarm.trajectory as tgen
import bswarm.formation as formation
import bswarm
import json

def plot_formation(F, name):
    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(F[0, :], F[1, :], F[2, :], 'ro')
    plt.title(name)
    ax.set_xlabel('x, m')
    ax.set_ylabel('y, m')
    ax.set_zlabel('z, m')
    plt.show()

def scale_formation(form, scale):
    formNew = np.copy(form)
    for i in range(3):
        formNew[i, :] *= scale[i]
    return formNew

#%% parameters

# defines how the drones are ordered for circles etc.
rotation_order = [4, 3, 2, 5, 0, 1]

# scaling for formation
form_scale = np.array([1.8, 1.8, 1])

#%% takeoff
formTakeoff = np.array([
    [-1, -1, 0],
    [0, 0, 0],
    [1, 1, 0],
]).T
n_drones = formTakeoff.shape[1]
plot_formation(formTakeoff, 'takeoff')

#%% 8
formEight = [
    [-1, -1, 0],
    [0, 0, 0],
    [1, 1, 0],
    [0,2,0],
    [-1,1,0],
    [0,0,0],
    [1,-1,0],
    [0,-2,0],
    [-1,-1,0],
    [0, 0, 0],
    [1, 1, 0],
]

formEightnum = np.array([
    [-1, -1, 0],
    [0, 0, 0],
    [1, 1, 0],
    [0,2,0],
    [-1,1,0],
    [0,0,0],
    [1,-1,0],
    [0,-2,0],
    [-1,-1,0],
    [0, 0, 0],
    [1, 1, 0],
])
plot_formation(formEightnum.T, 'formEight')

class Geometry:

    rgb = {
        'black': [0, 0, 0],
        'gold': [255, 100, 15],
        'red': [255, 0, 0],
        'green': [0, 255, 0],
        'blue': [0, 0, 255],
        'white': [255, 255, 255]
    }

    def __init__(self):
        self.waypoints = [formTakeoff]
        self.T = []
        self.delays = []
        self.colors = []

    def goto(self, form, duration, color):
        self.waypoints.append(form)
        self.T.append(duration)
        self.colors.append(self.rgb[color])
        n_drones = form.shape[1]
        self.delays.append(np.zeros(n_drones).tolist())
    
    def plan_trajectory(self):
        trajectories = []
        origin = np.array([1.5, 2, 2])
        waypoints = np.array(self.waypoints)
        for drone in range(waypoints.shape[2]):
            pos_wp = waypoints[:, :, drone] + origin
            yaw_wp = np.zeros((pos_wp.shape[0], 1))
            traj = tgen.min_deriv_4d(4, 
                np.hstack([pos_wp, yaw_wp]), self.T, stop=False)
            trajectories.append(traj)

        traj_json = tgen.trajectories_to_json(trajectories)
        data = {}
        for key in traj_json.keys():
            data[key] = {
                'trajectory': traj_json[key],
                'T': self.T,
                'color': g.colors,
                'delay': [d[key] for d in g.delays]
            }
        data['repeat'] = 2
        assert len(trajectories) < 32
        assert len(self.T) < 32
        return trajectories, data

# create trajectory waypoints
g = Geometry()

g.goto(form=formTakeoff, duration=0.1, color='blue')

c = 0

temp = []
for i in formEight:
    temp.append(i)
    temp.append(formEight[c+1])
    temp.append(formEight[c+2])
    print(temp)
    temp = np.asarray(temp).T
    plot_formation(temp, 'formEight')
    g.goto(form=temp, duration=2, color='black')

    if c+2 == 10:
        break

    c+=1
    temp = []

g.goto(form=formTakeoff, duration=1.7, color='blue')

#%% plan trajectories
trajectories, data = g.plan_trajectory()

with open('data/8config.json', 'w') as f:
    json.dump(data, f)

tgen.plot_trajectories(trajectories)
tgen.animate_trajectories('8config.mp4', trajectories, 1)

#%%
plt.figure()
tgen.plot_trajectories_time_history(trajectories)
plt.show()

#%%
plt.figure()
tgen.plot_trajectories_magnitudes(trajectories)
plt.show()

#%%
print('number of segments', len(trajectories[0].coef_array()))
#%%
plt.figure()
plt.title('durations')
plt.bar(range(len(g.T)), g.T)
plt.show()