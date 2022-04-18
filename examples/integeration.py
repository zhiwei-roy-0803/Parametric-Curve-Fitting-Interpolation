import numpy as np
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

def plot_simpson():
    nums = [100, 500, 1000, 2000, 5000, 10000]
    res = []
    for num in nums:
        res.append(Interpolator.simpson(curve1_x, 0, 1, num))
    import matplotlib.pyplot as plt
    plt.figure(dpi=300, figsize=(10, 8))
    plt.plot(nums, res, marker="o", linewidth=2)
    plt.xlabel("Grid Number")
    plt.ylabel("$\int_{0}^{1}x(u)du$")
    plt.grid(axis="y")
    plt.savefig("/res/simpson.pdf")

def plot_comparison():
    nums = [100, 500, 1000, 2000, 5000, 10000]
    res = {
        "simpson": [],
        "trapezoid": []
    }
    for num in nums:
        res["simpson"].append(Interpolator.simpson(curve1_x, 0, 1, num))
        res["trapezoid"].append(Interpolator.trapezoid(curve1_x, 0, 1, num))
    import matplotlib.pyplot as plt
    plt.figure(dpi=300, figsize=(10, 8))
    plt.plot(nums, res["simpson"], marker="o", linewidth=2)
    plt.plot(nums, res["trapezoid"], marker="*", linewidth=2)
    plt.xlabel("Grid Number")
    plt.ylabel("$\int_{0}^{1}x(u)du$")
    plt.grid(axis="y")
    plt.legend(["Simpson", "Trapezoid"])
    plt.savefig("//res/comparison.pdf")


if __name__ == "__main__":
    plot_comparison()

