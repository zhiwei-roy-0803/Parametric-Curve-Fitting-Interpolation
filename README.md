# Parametric-Curve-Fitting&Interpolation
This project is for implementing various of numerical algorithms
over a parametric curve, including Least Square approximiation,
cubic B-Spline interpolation, trigonometric interpolation,
numerical integration etc.
This is for the assigent 2 for the CE7453
Numerical Algorithms in NTU, Singapore

# Implemented Curve Fitting (Interpolation) Method

* Polynomial Least Square

* Cubic B-spline

* Trigonometric Interpolation

# Implemented Numerical Integration Method
* Composite Simpson's rule

* Composite Trapezoid's rule

# How to use
* Step 1: Interpolation result visualization
  * To see the interpolation or fitting result, just run the following command
    ```bash
    cd examples
    python visulation.py
    ```
The visulation.py is the entry for the three interpolation/fitting method.
By running it, you can get the interpolation/fitting result for all these
methods and they will be store into the /examples/res directory.

* Step 2: Numerical integration result comparison
  * Run the following command
  ```bash
  cd examples
  python intergration.py
  ```
    By running the code, you will get the convergence behavior curve both
    the Composite Simpson's rule and the Composite Trapozoid's rule, as well
    as their comparison result. The result will be stored in to the examples/res directory

# Technical Details

We provide the technical document for the parametric curve interpolation/fitting algorithm
in ./docs directory. Please refer to the document for the technical details.
