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

    p = 1
    
    model = gp.Model('TrnLocMILP')

    y0 = model.addVar(vtype='C', name="y0")
    
    # Variables
    y = {}
    z = {}
    
    for i in R:
        y[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "y[%s]" % i)

    for i in R:
        z[i] = model.addVar(vtype=GRB.BINARY, name = "z[%s]" % i)

    # Constraints
    Probability = {}
    Y_constrain = {}
    Z_constrain = {}
    for i in R:
        Probability[i] = model.addConstr(
            y0 + gp.quicksum(y[i] for i in R) == 1
        )
    n=0
    for j in R:
        Y_constrain[j] = model.addConstr(
            y[j] <= y0*exp(Mu[n])
        )
        n+=1

    for j in R:
        Z_constrain[j] = model.addConstr(y[j] <= z[j])

    for i in range(n):
        model.addConstr(gp.quicksum(z[i]) <= p)
    
    model.update()
    model.setObjective(gp.quicksum(i*y[i] for i in R), GRB.MAXIMIZE)
    model.update()
    return model


# Retrieve the data form the CSV file, r => the net revenue of the object i where i belongs to I
#                                      mu => the mean utilities of the object i

data = {}
data['R'] = read_data(os.path.join('data', 'small-r.csv'))
data['Mu'] = read_data(os.path.join('data', 'small-mu.csv'))

model_AssPlan = Ass_Plan_Prob(data,10)
model_AssPlan.optimize()
