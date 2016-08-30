import numpy as np
import scipy.optimize as opt

a=20 # y intercept
b=5 #negative slope
def objective(x, sign=1.0): #create objective function. can change sign argument if want to minimize
    yzero=a-b*x[0] #height of first reactangle 
    yone=a-b*x[1]
    ytwo=a-b*x[2]
    return sign*(x[0]*yzero + x[1]*(yone-yzero) +x[2]*(ytwo-yone)) 

def derivative(x, sign=1.0):
    dfdx0 = sign*(b*((a/b)-2*x[0]+x[1]))
    dfdx1=sign*(b*(x[0]-2*x[1]+x[2]))
    dfdx2=sign*(b*(x[1]-2*x[2]))
    return np.array([ dfdx0, dfdx1, dfdx2 ])




def maxconstraint(x): # first x (x[0] cant be bigger than 4)
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
         'jac' : jac1
         },
         {'type': 'ineq',
         'fun' : zeroconstraint,
         'jac' : jaczer},
         {'type': 'ineq',
         'fun' : limitxone,
         'jac' : jaclimitone},
         {'type': 'ineq',
         'fun' : limitxtwo,
         'jac' : jaclimittwo})

# cons = ({'type': 'ineq',
#          'fun' : lambda x: np.array([a/b - x]),
#          'jac' : lambda x: np.array([-1.0])
#          })

# constrained
result = opt.minimize(objective, [1,.09,.1], args=(-1), jac=derivative,
                      constraints=cons, method='SLSQP', options={'disp': True})

print("constrained: {}".format(result.x))