import numpy as np
import matplotlib.pyplot as plt
from typing import List
from src.approximater.least_square import LeastSquareEstimator
from src.interpolater.spline.cubic import CubicBSpline
from src.interpolater.trigonometric.trigo_interpolator import TrigoInterpolator
from src.utils.sampler import ParametricCurveSampler
from src.utils.curve import curve1_x, curve1_y


def eval_curve(u: np.ndarray) -> List[np.ndarray]:
    x = curve1_x(u)
    y = curve1_y(u)
    return [x, y]


def polynomial_least_square(X: np.ndarray, Y: np.ndarray, degree=3) -> LeastSquareEstimator:
    approximator = LeastSquareEstimator(degree=degree)
    approximator.fit(X, Y)
    return approximator

def cubic_bspline(X: np.ndarray, Y: np.ndarray) -> CubicBSpline:
    num_samples = len(X)
    points = np.zeros((num_samples, 2))
    points[:, 0] = X
    points[:, 1] = Y
    approximator = CubicBSpline(points=points, ndim=2)
    approximator.find_control_points()
    return approximator


def plot_cubic_bspline(num_sample: int):
    u, x, y = ParametricCurveSampler.sample(number_sample=num_sample, method="uniform")
    approximator = cubic_bspline(x, y)
    tt = np.linspace(start=0.0, stop=0.999, num=100)
    x_hat, y_hat = approximator.eval(tt)
    plt.figure(dpi=300)
    plt.plot(x_hat, y_hat)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(axis="y")
    plt.savefig("examples/res/BSpline-100.pdf")


def plot_polynomial_least_square(num_sample: int, num_degree : int):

    u, x, y = ParametricCurveSampler.sample(number_sample=num_sample, method="uniform")

    estimator_x = polynomial_least_square(u, x, num_degree)
    estimator_y = polynomial_least_square(u, y, num_degree)

    u = np.linspace(0, 0.999, 100)

    x_hat = estimator_x.eval(u)
    y_hat = estimator_y.eval(u)


    plt.figure(dpi=300)
    plt.plot(x_hat, y_hat)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(axis="y")
    plt.savefig("examples/res/Degree-50.pdf")

    plt.figure(dpi=300)
    plt.subplot(121)
    plt.plot(u, x_hat)
    plt.xlabel("u")
    plt.ylabel("x")
    plt.grid(axis="y")
    plt.subplot(122)
    plt.plot(u, y_hat)
    plt.xlabel("u")
    plt.ylabel("y")
    plt.grid(axis="y")

    # plt.show()


def plot_exact():

    u = np.linspace(0, 1.0, 100)

    x, y = eval_curve(u)

    plt.figure(dpi=300)
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(axis="y")
    plt.savefig("examples/res/exact.pdf")

def plot_trigo_interpolation(num_sample: int):

    u, x, y = ParametricCurveSampler.sample(number_sample=num_sample, method="uniform")

    trigo_interpolator = TrigoInterpolator(order=num_sample)

    dft_x = trigo_interpolator._dft(x)
    dft_y = trigo_interpolator._dft(y)

    u = np.linspace(0, 0.999, 100)

    x_hat = trigo_interpolator.interpolate(u, dft_x)
    y_hat = trigo_interpolator.interpolate(u, dft_y)

    x_exact, y_exact = eval_curve(u)

    plt.figure(dpi=300)
    plt.plot(x_hat, y_hat)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(axis="y")

    plt.savefig(f"examples/res/Trigo-{num_sample}.pdf")

    plt.figure(dpi=300)
    plt.plot(u, x_hat)
    plt.plot(u, x_exact)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(["trigonometric", "exact"])
    plt.grid(axis="y")

    plt.show()


if __name__ == "__main__":
    plot_exact()
    plot_polynomial_least_square(num_sample=1000, num_degree=50)
    plot_cubic_bspline(num_sample=100)
    plot_trigo_interpolation(num_sample=32)