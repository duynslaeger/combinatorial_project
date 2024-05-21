import csv
import os
import gurobipy as gp
from math import exp
from gurobipy import GRB
import numpy as np
import matplotlib.pyplot as plt


def read_data(file):
    data = []
    with open(file, newline='') as csvfile:
        column = csv.reader(csvfile, delimiter=';')
        for row in column:
            data.extend([float(value) for value in row])
    return data

def APC_MILP(data):
    # Unpack
    R = data['R']
    Mu = data['Mu']
    I = [i for i in range(len(R))]

    # Change here the probability --> Not a proba ! p is the number of objects. p \in {1, n/5, n/2, n}
    p = len(I)/5
    
    model = gp.Model('APC_MILP')

    # First add the variables that you use
    # y = model.addVars(len(R),vtype=GRB.CONTINUOUS, name = "y", lb=0)
    # z = model.addVars(len(R),vtype=GRB.BINARY, name = "z")
    
    # That's the code from the lab
    # however there are strange because you build your dictionnary with key equals to the value of R ?
    # like y={"0.0":1, "0.0":2,...}

    # Variables
    y = {}
    z = {}
    
    for i in I:
        y[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "y[%s]" % i, lb=0)

    for i in I:
        z[i] = model.addVar(vtype=GRB.BINARY, name = "z[%s]" % i)

    # 4 Constraints
    Probability = {}
    Y_constrain = {}
    Z_constrain = {}
    Unknow_constrain = {}


    # for i in I:
    #     Probability[i] = model.addConstr(
    #         y[0] + gp.quicksum(y[i]) == 1
    #     )

    for i in I:
        Y_constrain[i] = model.addConstr(
            y[i] <= y[0]*exp(Mu[i])
        )

    for i in I:
        Z_constrain[i] = model.addConstr(y[i] <= z[i])

    # for i in I:
    #     Unknow_constrain[i] = model.addConstr(gp.quicksum(z[i]) <= p)

    # Second add the constraint of your model
    model.addConstr(y[0]+gp.quicksum(y[i] for i in I) == 1) # Need to remove i=0
    # model.addConstrs(y[i] <= y[0]*exp(Mu[i]) for i in I)
    # model.addConstrs(y[i] <= z[i] for i in I)
    model.addConstr(gp.quicksum(z[i] for i in I) <= p ) #need to remove i=0
    
    # Then set the objective function
    model.setObjective(R[0]*y[0] + gp.quicksum(R[i]*y[i] for i in I[1:]), GRB.MAXIMIZE)
    # Update the model
    model.update()


    # Otpimize it
    model.optimize()
    print("Optimization is done. Objective function Value: %.2f " % model.ObjVal)

    # Get the optimal values of y
    optimal_y = [y[i].getAttr('X') for i in range(len(R))]

    # Get the optimal values of z
    optimal_z = [int(z[i].getAttr('X')) for i in range(len(R))]

    fig, axs = plt.subplots(2)
    fig.suptitle('Solution problem')

    axs[0].scatter([i for i in range(len(R))],optimal_y)
    axs[1].scatter([i for i in range(len(R))],optimal_z)
    plt.show()

    return model

# Retrieve the data from the CSV file, r => the net revenue of the object i where i belongs to I
#                                      mu => the mean utilities of the object i

data = {}
data['R'] = read_data(os.path.join('data', 'small-r.csv'))
data['Mu'] = read_data(os.path.join('data', 'small-mu.csv'))
model_AssPlan = APC_MILP(data)
print(model_AssPlan.getAttr('X'))
