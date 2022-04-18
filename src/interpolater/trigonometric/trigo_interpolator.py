import numpy as np


class TrigoInterpolator():

    def __init__(self, order):
        self.order = order

    def _dft(self, x:np.ndarray):
        '''
        Implement Discrete Fourier Transform (DFT)
        :param x:
        :return:
        '''
        n = len(x)
        w = np.complex(real=np.cos(2*np.pi/n), imag=np.sin(-2*np.pi/n))
        y = np.zeros_like(x, dtype=np.complex)
        for j in range(n):
            wj = w**j
            tmp = 0
            for k, xk in enumerate(x):
                tmp += xk * wj**k
            y[j] = 1/np.sqrt(n) * tmp

        return y

    def interpolate(self, u:np.ndarray, dft:np.ndarray):
        n = len(dft)
        sqrt_n = np.sqrt(n)
        a = dft.real
        b = dft.imag
        c = np.min(u)
        d = np.max(u)
        a0 = a[0]
        a_n_2 = a[n//2]
        res = np.zeros_like(u)
        for i, val in enumerate(u):
            tmp = a0/sqrt_n
            for k in range(1, n//2 - 1):
                tmp += 2/sqrt_n * (a[k] * np.cos(2*np.pi*(val - c)/(d - c)*k) - b[k] * np.sin(2*np.pi*(val - c)/(d - c)*k))
            tmp += a_n_2/sqrt_n*np.cos(np.pi*(val - c)/(d - c)*n)
            res[i] = tmp
        return res





