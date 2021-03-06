# -*- coding: utf-8 -*-
"""Odd Polynomial Fitting.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18XhvH9qgWAf0KfFO69W1Kdm29B2kOKi2
"""

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [20, 15]

def polynomial_fitted_y_values(x, w):
    x = [x ** j for j in np.arange(0, w.size)]
    wTx = w[:, np.newaxis].T.dot(x).T
    return wTx[:, 0]


def least_squares(M, x, t):
        
    x_domain = np.array([x ** j for j in np.arange(0, M + 1)])
    xOdd = x_domain.copy()
    #xOdd = xOdd.tolist()
    index = []
    for i in range(x_domain.shape[0]):
      if i % 2 == 0:
        index.append(i)
    if M == 0:
        xOdd[i] = np.nan
    else:
      xOdd = np.delete(x_domain, index, 0)
    
    return np.linalg.solve(xOdd.dot(xOdd.T), xOdd.dot(t))

def main():
  
    x = np.linspace(-10, 10, 21)
    
    t =  np.array([erf(xVal) for xVal in x])
    xs = np.linspace(-10, 10, 500)
    t_ideal = np.array([erf(xVal) for xVal in xs])
    l2_diff = []
    rms_diff = []
    abs_errors = []
       
    M = np.arange(1, 10).reshape(-1)
    fig_row = np.ceil(M.shape[0] / 2)
    fig_col = np.ceil(len(M) / fig_row)
    fig = plt.figure()
    for i, m in enumerate(M):
        index = []
        w = least_squares(m, x, t)
        # index for all the even coefficient
        index = np.arange(0, len(w))
        # padding w with zero's in the even coefficient position
        w = np.insert(w, index, 0) 
        rms_error = rmse(polynomial_fitted_y_values(xs, w), t_ideal)
        abs_error = absolute_error(polynomial_fitted_y_values(xs, w), t_ideal)

        # l2_norm = np.linalg.norm((t_ideal - polynomial_fitted_y_values(xs, w)), 2)

        # l2_diff.append(l2_norm)
        rms_diff.append(rms_error)
        abs_errors.append(abs_error)
        
        fig.add_subplot(fig_row, fig_col, i + 1)
        plt.plot(x, t, 'b.', label='Training data', markersize = 12)
        plt.plot(xs, t_ideal, 'g-', label='f(x) = erf(x)')
        plt.plot(xs, polynomial_fitted_y_values(xs, w), 'r-', label='Polynomial Curve fitting')
        plt.legend()
        plt.title('M = {0}'.format(m))
        plt.xlim(-10, 10)
        plt.ylim(-6.5, 6.5)
    
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(10, 5))
    ax1.plot(np.arange(1, 10), abs_errors, marker='o', label='Absolute Error')
    ax2.plot(np.arange(1, 10), rms_diff, marker="*", label='RMSE')
    ax1.set_title('Degree vs. Absolute Error')
    ax2.set_title('Degree vs. RMSE')
    ax1.set_xlabel('n = Degree')
    ax2.set_xlabel('n = Degree')
    ax1.set_ylabel('Error')
    ax2.set_ylabel('Error')
    plt.legend()

    plt.xticks(np.arange(0,10,1))
    plt.show()        

if __name__ == '__main__':
  main()