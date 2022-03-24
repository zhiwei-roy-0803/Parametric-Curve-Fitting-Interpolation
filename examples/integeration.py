import scipy.integrate
from src.integrator.integrator import Interpolator
from src.utils.curve import curve1_x


def integrate(num=10**6):
    res_simpson = Interpolator.simpson(curve1_x, 0, 1, num)
    res_trapezoid = Interpolator.trapezoid(curve1_x, 0, 1, num)
    res_scipy = scipy.integrate.quad(curve1_x, 0, 1)[0]
    print("Integration with composite Simpson: {:.6f}".format(res_simpson))
    print("Integration with composite Trapezoid: {:.6f}".format(res_trapezoid))
    print("Integration with Scipy Quad: {:.6f}".format(res_scipy))

if __name__ == "__main__":
    integrate()

