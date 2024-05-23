import gurobipy as gp
from gurobipy import GRB
from AP_problem import read_data
from math import exp
from matplotlib import pyplot as plt


def AP_L_Lambda(Mu, R, p, lambd):
    I = [i for i in range(len(R))]
    
    model = gp.Model('AP_L_Lambda')
    model.setParam('OutputFlag', 0)

    # Variables
    y = {}
    
    for i in I:
        y[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "y[%s]" % i, lb=0)

    Y_constrain = {}

    for i in I[1:]:
        Y_constrain[i] = model.addConstr(
            y[i] <= y[0]*exp(Mu[i])
        )

    model.addConstr(y[0]+gp.quicksum(y[i] for i in I[1:]) == 1) # Need to remove i=0
    
    # Then set the objective function
    model.setObjective((R[0] + lambd*p)*y[0] + gp.quicksum((R[i] - (lambd/exp(Mu[i])))*y[i] for i in I[1:]), GRB.MAXIMIZE)
    # Update the model
    model.update()


    # Optimize it
    model.optimize()

    return model

def binary_search_lambda(Mu, R, p):
    # Mu and R are already from the willing instance
    max_right_bound = max(0, (R[1] - R[0])/p)
    if(max_right_bound == 0):
        return 0
    left_bound = 0
    right_bound = max_right_bound
    minNotFound = True

    # Heuristic, in order to keep the lambda that gives the best val
    bestLamba = round((right_bound - left_bound)/2,2)
    bestVal = AP_L_Lambda(Mu, R, p, bestLamba).ObjVal

    while(minNotFound):
        currLambda = round((right_bound - left_bound)/2,2)
        currVal = AP_L_Lambda(Mu, R, p, currLambda).ObjVal
        rightVal = AP_L_Lambda(Mu, R, p, currLambda+1e-12).ObjVal
        # Heuristic : 
        if(currVal > bestVal):
            bestLamba = currLambda
            bestVal = currVal

        # First stopping criteria, if lambda has reached its minimal value
        if(currLambda == 0.0):
            minNotFound = False
            break

        if(currVal < rightVal):
            # Search on the left
            right_bound = currLambda
        elif(currVal > rightVal):
            # Sarch on the right
            left_bound = currLambda
        # Second stopping criteria, if lambda has reached its optimal value
        else:
            minNotFound = False

    return currLambda, currVal, bestLamba, bestVal


m = 100
x = [i for i in range(1,m+1)]
small_primal_bounds = []
small_dual_bounds = []
medium_primal_bounds = []
medium_dual_bounds = []

# -------------- small --------------

data = read_data('small')

for i in range(m):
    p = len(data['R'][i])
    lambdaStar, minVal, bestLambda, bestVal = binary_search_lambda(data['Mu'][i], data['R'][i], p)
    small_primal_bounds.append(bestVal)
    small_dual_bounds.append(minVal)

plt.title("Bounds on small instances")
plt.plot(x, small_primal_bounds, label="Primal bounds")
plt.plot(x, small_dual_bounds, label="Dual Bounds")
plt.xlabel('Instances')
plt.ylabel("Objective value")
plt.legend()
plt.savefig('results/small_bounds.png')
plt.clf()
# plt.show()


# -------------- medium --------------

data = read_data('medium')

for i in range(m):
    p = len(data['R'][i])
    lambdaStar, minVal, bestLambda, bestVal = binary_search_lambda(data['Mu'][i], data['R'][i], p)
    medium_primal_bounds.append(bestVal)
    medium_dual_bounds.append(minVal)

plt.title("Bounds on medium instances")
plt.plot(x, medium_primal_bounds, label="Primal bounds")
plt.plot(x, medium_dual_bounds, label="Dual Bounds")
plt.xlabel('Instances')
plt.ylabel("Objective value")
plt.legend()
plt.savefig('results/medium_bounds.png')


