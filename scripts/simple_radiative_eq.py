import matplotlib.pyplot as plt
import numpy as np

#%% Define general parameters

s0 = 1370
sigma = 5.67e-8
alpha = 0.3

#%% Simple two layer atmospheric slabs
ylist = [0, 1, 2]
labels = ['surface', 'layer 1', 'layer 2']

# Compute temperatures
t1 = (s0 * (1-alpha) / (4*sigma)) ** 0.25
t2 = (2) ** 0.25 * t1
ts = (3) ** 0.25 * t1

# Initialize plot
fig, ax = plt.subplots()

# Plot
plt.plot([ts, t2, t1], ylist, label='simple model')
plt.yticks(ylist, labels)

#%% Distributing absorption of solar radiation

t1 = (s0 * (1-alpha) / (4*sigma)) ** 0.25
t2 = (1.7) ** 0.25 * t1
ts = (2.1) ** 0.25 * t1

# Plot
plt.plot([ts, t2, t1], ylist, label='model with solar absorption in atmosphere')
plt.xlabel('temperature [K]')
plt.grid()
plt.legend()
plt.savefig('./output/slab_model.png')
