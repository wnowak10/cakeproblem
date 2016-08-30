import numpy as np
import scipy.optimize as opt
import math

# can wolfram do it?
# maximize (x^2)* (10-5*x) + (y^2)((10-5y) - (10-5x)) + (z^2)*((10-5z) - (10-5y)) on z<y<x<2

a=20 # y intercept
b=5 #negative slope
def objective(x, sign=1.0): #create objective function. can change sign argument if want to minimize
    yzero=a-b*x[0] #height of first cylinder 
    yone=a-b*x[1]
    ytwo=a-b*x[2]
    return sign*(yzero*(x[0]**2) + (yone-yzero)*(x[1]**2) + (ytwo-yone))*(x[2]**2) # volume of 3 cylinders
    # leave out pi as constant doesnt affect optimization

def derivative(x, sign=1.0):
    dfdx0 = sign*(2*a*x[0]-3*b*(x[0]**2)+b*(x[1]**2)) #used wolfram alpha to help
    # d/dx (x^2)* (a-b*x) + (y^2)((a-by) - (a-bx)) + (z^2)*((a-bz) - (a-by))
    dfdx1=sign*(b*(2*x[0]*x[1] - 3*(x[1]**2) + (x[2]**2)))   
    dfdx2=sign*b*x[2]*(2*x[1]-3*x[2])
    return np.array([ dfdx0, dfdx1, dfdx2 ])




def maxconstraint(x): # first x (x[0] cant be bigger than a/b)
    return np.array([(a/b)-x[0]])

def jac1(x): # derivative
    return np.array([-1,0,0])

def zeroconstraint(x): # smallest x has to be greater than 0 ( x[2] > 0 )
	return np.array([x[2]])

def jaczer(x):
	return np.array([0,0,1])

def limitxone(x): # x[0] > x[1]
    return np.array([x[0]-x[1]])
    
def jaclimitone(x):
    return np.array([1,-1,0])

def limitxtwo(x): # x[1] > x[2]
    return np.array([x[1]-x[2]])

def jaclimittwo(x):
    return np.array([0,1,-1])


cons = ({'type': 'ineq',
         'fun' : maxconstraint,
         'jac' : jac1},
         {'type': 'ineq',
         'fun' : zeroconstraint,
         'jac' : jaczer},
         {'type': 'ineq',
         'fun' : limitxone,
         'jac' : jaclimitone},
         {'type': 'ineq',
         'fun' : limitxtwo,
         'jac' : jaclimittwo})



# constrained [.3,.2,.01]
result = opt.minimize(objective,[3.5,2.9,1], args=(-1), jac=derivative,
                       method='SLSQP', options={'disp': True,'maxiter': 10000})

print("constrained: {}".format(result.x))