import numpy as np
from src.utils.curve import curve1_x, curve1_y

class ParametricCurveSampler():

    def __init__(self):
        pass

    @staticmethod
    def sample(number_sample, method="uniform"):
        sample_funcs = {
            "uniform": lambda s: np.linspace(0.0, 1.0, s),
            "random": lambda s: np.random.uniform(low=0.0, high=1.0, size=s)
        }
        u = sample_funcs[method](number_sample)
        return u, curve1_x(u), curve1_y(u)
