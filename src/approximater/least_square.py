import numpy as np

class LeastSquareEstimator():

    def __init__(self, degree:int = 3):
        self.degree = degree


    def _eval_polynomial(self, X: np.ndarray, k: int) -> np.ndarray:
        return X**k


    def fit(self, X: np.ndarray, Y: np.ndarray) -> None:
        num_samples = len(X)
        A = np.zeros((num_samples, self.degree + 1))
        for i, k in enumerate(range(self.degree, -1, -1)):
            A[:, i] = self._eval_polynomial(X, k)
        b = Y
        # solve The Least Square problem by solve the linear system (A^T*A) * v = A^T * y to find coefficients vector v
        self.p = np.linalg.solve(np.dot(A.T, A), np.dot(A.T, b))


    def eval(self, X: np.ndarray) -> np.ndarray:
        return np.polyval(p=self.p, x=X)