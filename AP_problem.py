import csv
import os
import gurobipy as gp
from math import exp
from gurobipy import GRB
import numpy as np


def read_data(file):
    data = []
    with open(file, newline='') as csvfile:
        column = csv.reader(csvfile, delimiter=';')
        for row in column:
            data.extend([float(value) for value in row])
    return data

def Ass_Plan_Prob(data,n):
    # Unpack
    R = data['R']
    Mu = data['Mu']

    # Change here the probability
    p = len(R)/5
    
    model = gp.Model('TrnLocMILP')

    # First add the variables that you use
    y = model.addVars(len(R),vtype=GRB.CONTINUOUS, name = "y", lb=0)
    z = model.addVars(len(R),vtype=GRB.BINARY, name = "z")
    
    # That's the code from the lab
    # however there are strange because you build your dictionnary with key equals to the value of R ?
    # like y={"0.0":1, "0.0":2,...}

    # Variables
    # y = {}
    # z = {}
    
    # for i in R:
    #     y[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "y[%s]" % i, lb=0)

    # for i in R:
    #     z[i] = model.addVar(vtype=GRB.BINARY, name = "z[%s]" % i)

    # Constraints
    Probability = {}
    Y_constrain = {}
    Z_constrain = {}


    # for i in R:
    #     Probability[i] = model.addConstr(
    #         y0 + gp.quicksum(y[i] for i in R) == 1
    #     )
    # n=0
    # for j in R:
    #     Y_constrain[j] = model.addConstr(
    #         y[j] <= y0*exp(Mu[n])
    #     )
    #     n+=1

    # for j in R:
    #     Z_constrain[j] = model.addConstr(y[j] <= z[j])

    # for i in range(n):
    #     model.addConstr(gp.quicksum(z[i]) <= p)

    # Second add the constraint of your model
    model.addConstr(y[0]+gp.quicksum(y[i] for i in range(len(R))) == 1)
    model.addConstrs(y[i] <= y[0]*exp(Mu[i]) for i in range(len(R)))
    model.addConstrs(y[i] <= z[i] for i in range(len(R)))
    model.addConstr(gp.quicksum(z[i] for i in range(len(R))) <= p )
    
    # Then set the objective function
    model.setObjective(R[0]*y[0] + gp.quicksum(R[i]*y[i] for i in range(1,len(R))), GRB.MAXIMIZE)
    # Update the model
    model.update()


    # Otpimize it
    model.optimize()
    print("Optimization is done. Objective function Value: %.2f " % model.ObjVal)

    # Get the optimal values of y
    optimal_y = [y[i].getAttr('X') for i in range(len(R))]

    # Get the optimal values of z
    optimal_z = [int(z[i].getAttr('X')) for i in range(len(R))]

    print(optimal_y)
    print(optimal_z)

    return model

# Retrieve the data form the CSV file, r => the net revenue of the object i where i belongs to I
#                                      mu => the mean utilities of the object i

data = {}
data['R'] = read_data(os.path.join('data', 'small-r.csv'))
data['Mu'] = read_data(os.path.join('data', 'small-mu.csv'))

model_AssPlan = Ass_Plan_Prob(data,10)
