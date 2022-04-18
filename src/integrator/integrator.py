import numpy as np
from typing import Callable

class Interpolator():

    @staticmethod
    def trapezoid(f: Callable, a: float, b: float, m: int) -> float:
        h = (b - a) / m
        x = np.linspace(start=a, stop=b, num=m)
        return h/2 * (f(a) + f(b) + 2*np.sum(f(x[:-1])))

    @staticmethod
    def simpson(f: Callable, a: float, b: float, m: int) -> float:
        assert a <= b
        h = (b - a) / (2 * m)
        x = np.linspace(start=a, stop=b, num=2*m)
        x_odd = x[0:-1:2]
        x_even = x[1::2]
        return h/3 * (f(a) + f(b) + 4*np.sum(f(x_odd)) + 2*np.sum(f(x_even)))