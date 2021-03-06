import numpy as np
from src.interpolater.spline.basis import basis_func, basis_derivative2
from src.interpolater.solver.scipy_wrapper import ScipyWrapper
from src.interpolater.solver.tridiagonal import TriDiagonalSolver


class CubicBSpline():

    def __init__(self, points: np.ndarray, ndim: int = 2):
        self.points = points
        self.ndim = ndim
        self.num_points = len(points)
        self.n = self.num_points - 1


    def _parameterize(self, method="chord"):
        func_dict = {
            "uniform": self._uniform,
            "chord": self._chord
        }
        return func_dict[method]()


    def _uniform(self):
        '''
        parameterize the curve uniformly
        :return:
        '''
        return np.linspace(0, 1, self.num_points + 1)


    def _chord(self):
        '''
        parameterize the curve using chord length
        :return:
        '''
        t = np.zeros(self.num_points)
        dist = np.linalg.norm(self.points[1:] - self.points[:-1], axis=1)
        t[1:-1] = np.cumsum(dist)[:-1]/np.sum(dist)
        t[-1] = 1.0
        return t


    def _build_linear_system(self, coordinates, knot):
        A = np.zeros((self.n + 3, self.n + 3))
        b = np.zeros(self.n + 3)

        # Step 1: set the first and last diagonal component in matrix A as 1
        A[0, 0] = A[-1, -1] = 1.0

        # Step 2: for the i-th input data point except for the first and the last one, eval corresponding cubic basis
        # func (3 terms) and place the eval results into the (i + 1)-th row
        for i in range(2, self.n + 1):
            x = knot[i + 2]
            a1 = basis_func(T=knot[i - 1:i + 4], x=x)
            a2 = basis_func(T=knot[i:i + 5], x=x)
            a3 = basis_func(T=knot[i + 1:i + 6], x=x)
            A[i, i - 1] = a1
            A[i, i] = a2
            A[i, i + 1] = a3

        # Step 3: establish C2 continuity equation for the two boundary points, put the corresponding coefficients in
        # the second the penultimate row
        t0 = 0.0
        A[1, 0] = basis_derivative2(T=knot[0:5], x=t0)
        A[1, 1] = basis_derivative2(T=knot[1:6], x=t0)
        A[1, 2] = basis_derivative2(T=knot[2:7], x=t0)
        tn = 1.
        A[-2, -3] = basis_derivative2(T=knot[self.n:self.n+5], x=tn)
        A[-2, -2] = basis_derivative2(T=knot[self.n+1:self.n+6], x=tn)
        A[-2, -1] = basis_derivative2(T=knot[self.n+2:self.n+7], x=tn)

        # Step 4: place data point at the suitable place in vector b
        b[0] = coordinates[0]
        b[-1] = coordinates[-1]
        b[2:-2] = coordinates[1:-1]

        return [A, b]

    def _Nik(self, u, knots, i, k):
        '''
        Evaluate Cubic B-Spline basis function recursively
        :param u:
        :param knots:
        :param i:
        :param k:
        :return:
        '''
        if k == 0:
            return 1.0 if knots[i] <= u < knots[i + 1] else 0.0
        if knots[i + k] == knots[i]:
            c1 = 0.0
        else:
            c1 = (u - knots[i]) / (knots[i + k] - knots[i]) * self._Nik(u, knots, i, k - 1)
        if knots[i + k + 1] == knots[i + 1]:
            c2 = 0.0
        else:
            c2 = (knots[i + k + 1] - u) / (knots[i + k + 1] - knots[i + 1]) * self._Nik(u, knots, i + 1, k - 1)
        return c1 + c2

    def find_control_points(self, solver_method="tridiagonal"):

        solvers = {
            "tridiagonal": TriDiagonalSolver.solve,
            "scipy": ScipyWrapper.solve
        }

        # Step 1: parameterize the curve
        t = self._parameterize()

        # Step 2: set knot vector
        t0 = t[0]
        tn = t[-1]
        self.knots = np.zeros(4 + 4 + self.num_points - 2)
        self.knots[:4] = t0
        self.knots[-4:] = tn
        self.knots[4:-4] = t[1:-1]

        # Step 3: build matrix and solve matrix with a linear system solver to find the required de Boor points
        self.deBoor_points = np.zeros((self.n + 3, self.ndim))
        for dim in range(self.ndim):
            A, b = self._build_linear_system(self.points[:, dim], self.knots)
            self.deBoor_points[:, dim] = solvers[solver_method](A, b)


    def eval(self, us, degree=3):
        n = len(self.deBoor_points)
        num_eval_points = len(us)
        res = np.zeros((num_eval_points, 2))
        for idx, u in enumerate(us):
            val = np.zeros(2)
            for i in range(n):
                val += self.deBoor_points[i] * self._Nik(u, self.knots, i, degree)
            res[idx, :] = val
        return res[:, 0], res[:, 1]

