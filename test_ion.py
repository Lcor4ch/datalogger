import matplotlib.pyplot as plt
import numpy as np

F = lambda x: np.sin(2*x)

plt.ion()
x = np.linspace(0, 1, 200)
plt.plot(x, F(x))


for i in range(100):
    if 'ax' in globals(): ax.remove()
    newx = np.random.choice(x, size = 10)
    ax = plt.scatter(newx, F(newx))
    plt.pause(0.05)

plt.ioff()
plt.show()
