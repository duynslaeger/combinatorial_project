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


class AP():

    def __init__(self, data):
        self.R = data['R']
        self.Mu = data['Mu']
    
    def AP_IPL(self):
        # Unpack
        I = [i for i in range(len(self.R))]
        
        model = gp.Model('AP_IPL')

        # Variables
        y = {}
        
        for i in I:
            y[i] = model.addVar(vtype=GRB.SEMIINT, name = "y[%s]" % i, lb=0)

        # Second add the constraint of your model
        model.addConstr(y[0]+gp.quicksum(y[i] for i in I) == 1) # Need to remove i=0
        # model.addConstrs(y[i] <= y[0]*exp(Mu[i]) for i in I)
        # model.addConstrs(y[i] <= z[i] for i in I)
        
        # Then set the objective function
        model.setObjective(self.R[0]*y[0] + gp.quicksum(self.R[i]*y[i] for i in I[1:]), GRB.MAXIMIZE)
        # Update the model
        model.update()


        # Otpimize it
        model.optimize()
        print("Optimization on AP-IPL is done. Objective function Value: %.2f " % model.ObjVal)


        return model

    def AP_LD(self):
        # Unpack
        self.R = data['R']
        self.Mu = data['Mu']
        I = [i for i in range(len(self.R))]
        
        model = gp.Model('AP_LD')

        # First add the variables that you use
        # y = model.addVars(len(R),vtype=GRB.CONTINUOUS, name = "y", lb=0)
        # z = model.addVars(len(R),vtype=GRB.BINARY, name = "z")

        # Variables
        pi = {}
        
        pi[0] = 0
        for i in I[1:]:
            pi[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "pi[%s]" % i, lb=0)

        pi_zero = model.addVar(vtype=GRB.CONTINUOUS, name="pi_zero")

        Pi_constrain = {}
        Pi_zero_constrain = {}

        for i in I:
            Pi_constrain[i] = model.addConstr(
                pi_zero - gp.quicksum(pi[i]*exp(self.Mu[i]) for i in I[1:]) >= self.R[0], name="Pi_zero_constrain[%i]" %i
            )

        for i in I:
            Pi_zero_constrain[i] = model.addConstr(
                pi_zero + pi[i] >= self.R[i]
            )

        model.setObjective(pi_zero, GRB.MINIMIZE)
        # Update the model
        model.update()


        # Otpimize it
        model.optimize()
        print("Optimization on AP-LD is done. Objective function Value: %.2f " % model.ObjVal)

        return model

    def AP_IP(self):
        # Unpack
        self.Mu = data['Mu']
        I = [i for i in range(len(self.R))]
        
        model = gp.Model('AP_IP')

        # First add the variables that you use
        # y = model.addVars(len(R),vtype=GRB.CONTINUOUS, name = "y", lb=0)
        # z = model.addVars(len(R),vtype=GRB.BINARY, name = "z")

        # Variables
        x= {}

        # Introduce a new variable to allow division by non-constant
        z= {}
        min_bound = 1
        max_bound = 1+sum((exp(self.Mu[i]) for i in I[1:]))
        
        for i in I[1:]:
            x[i] = model.addVar(vtype=GRB.BINARY, name = "x[%s]" % i)

        z = model.addVar(vtype=GRB.CONTINUOUS)

        model.addConstr(
                (1+gp.quicksum(x[i]*exp(self.Mu[i]) for i in I[1:]))*z == 1
            )

        model.setObjective((self.R[0] + gp.quicksum(x[i]*self.R[i]*exp(self.Mu[i]) for i in I[1:]))*z, GRB.MAXIMIZE)
        # Update the model
        model.update()


        # Otpimize it
        model.optimize()
        print("Optimization on AP-IP is done. Objective function Value: %.2f " % model.ObjVal)

        return model

    def AP_LD(self):
        # Unpack
        self.R = data['R']
        self.Mu = data['Mu']
        I = [i for i in range(len(self.R))]
        
        model = gp.Model('AP_LD')

        # First add the variables that you use
        # y = model.addVars(len(R),vtype=GRB.CONTINUOUS, name = "y", lb=0)
        # z = model.addVars(len(R),vtype=GRB.BINARY, name = "z")

        # Variables
        pi = {}
        
        pi[0] = 0
        for i in I[1:]:
            pi[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "pi[%s]" % i, lb=0)

        pi_zero = model.addVar(vtype=GRB.CONTINUOUS, name="pi_zero")

        Pi_constrain = {}
        Pi_zero_constrain = {}

        for i in I:
            Pi_constrain[i] = model.addConstr(
                pi_zero - gp.quicksum(pi[i]*exp(self.Mu[i]) for i in I[1:]) >= self.R[0], name="Pi_zero_constrain[%i]" %i
            )

        for i in I:
            Pi_zero_constrain[i] = model.addConstr(
                pi_zero + pi[i] >= self.R[i]
            )

        model.setObjective(pi_zero, GRB.MINIMIZE)
        # Update the model
        model.update()


        # Otpimize it
        model.optimize()
        print("Optimization on AP-LD is done. Objective function Value: %.2f " % model.ObjVal)

        return model

    def AP_L(self):
        # Unpack
        I = [i for i in range(len(self.R))]
        
        model = gp.Model('AP_L')

        # First add the variables that you use
        # y = model.addVars(len(R),vtype=GRB.CONTINUOUS, name = "y", lb=0)
        # z = model.addVars(len(R),vtype=GRB.BINARY, name = "z")

        # Variables
        y = {}
        
        for i in I:
            y[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "y[%s]" % i, lb=0)

        Y_constrain = {}

        for i in I:
            Y_constrain[i] = model.addConstr(
                y[i] <= y[0]*exp(self.Mu[i])
            )

        # Second add the constraint of your model
        model.addConstr(y[0]+gp.quicksum(y[i] for i in I[1:]) == 1) # Need to remove i=0
        # model.addConstrs(y[i] <= y[0]*exp(Mu[i]) for i in I)
        # model.addConstrs(y[i] <= z[i] for i in I)
        
        # Then set the objective function
        model.setObjective(self.R[0]*y[0] + gp.quicksum(self.R[i]*y[i] for i in I[1:]), GRB.MAXIMIZE)
        # Update the model
        model.update()


        # Otpimize it
        model.optimize()
        print("Optimization on AP-L is done. Objective function Value: %.2f " % model.ObjVal)

        return model

    def APC_MILP(self):
        # Unpack
        self.R = data['R']
        self.Mu = data['Mu']
        I = [i for i in range(len(self.R))]

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
                y[i] <= y[0]*exp(self.Mu[i])
            )

        for i in I:
            Z_constrain[i] = model.addConstr(y[i] <= z[i])

        # for i in I:
        #     Unknow_constrain[i] = model.addConstr(gp.quicksum(z[i]) <= p)

        # Second add the constraint of your model
        model.addConstr(y[0]+gp.quicksum(y[i] for i in I[1:]) == 1) # Need to remove i=0
        # model.addConstrs(y[i] <= y[0]*exp(Mu[i]) for i in I)
        # model.addConstrs(y[i] <= z[i] for i in I)
        model.addConstr(gp.quicksum(z[i] for i in I[1:]) <= p ) #need to remove i=0
        
        # Then set the objective function
        model.setObjective(self.R[0]*y[0] + gp.quicksum(self.R[i]*y[i] for i in I[1:]), GRB.MAXIMIZE)
        # Update the model
        model.update()


        # Otpimize it
        model.optimize()
        print("Optimization on APC-MILP is done. Objective function Value: %.2f " % model.ObjVal)

        # Get the optimal values of y
        # optimal_y = [y[i].getAttr('X') for i in I]

        # # Get the optimal values of z
        # optimal_z = [int(z[i].getAttr('X')) for i in I]

        # fig, axs = plt.subplots(2)
        # fig.suptitle('Solution problem')

        # axs[0].scatter([i for i in I],optimal_y)
        # axs[1].scatter([i for i in I],optimal_z)
        # plt.show()

        return model

# Retrieve the data from the CSV file, r => the net revenue of the object i where i belongs to I
#                                      mu => the mean utilities of the object i

data = {}
data['R'] = read_data(os.path.join('data', 'small-r.csv'))
data['Mu'] = read_data(os.path.join('data', 'small-mu.csv'))

Problem_Ap = AP(data=data)
# model_AP_MILP = Problem_Ap.APC_MILP()
# print(model_AP_MILP.getAttr('X'))
# model_AP_L= Problem_Ap.AP_L()
# print(model_AP_L.getAttr('X'))
# model_AP_LD= Problem_Ap.AP_LD()
# for v in model_AP_LD.getVars():
#     if (v.VarName == "pi_zero"):
#         print(f"{v.VarName} = {v.X}")
# print(model_AP_LD.getAttr('X'))
# model_AP_IP= Problem_Ap.AP_IP()
# print([j.X for j in model_AP_IP.getVars()])
# for v in model_AP_IP.getVars():
#     print(f"{v.VarName} = {v.X}")
model_AP_IPL= Problem_Ap.AP_IPL()
print([j.X for j in model_AP_IPL.getVars()])