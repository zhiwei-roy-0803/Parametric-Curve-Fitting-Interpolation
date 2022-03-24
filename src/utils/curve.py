import numpy as np

h = 5

curve1_x = lambda u: 1.5 * (np.exp(1.5 * (np.sin(6.2 * u - 0.027 * h))) + 0.1) * np.cos(12.2 * u)
curve1_y = lambda u: (np.exp(np.sin(6.2 * u - 0.027 * h)) + 0.1) * np.sin(12.2 * u)