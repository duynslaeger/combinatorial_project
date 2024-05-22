import csv
import os
import gurobipy as gp
from math import exp
from gurobipy import GRB
import numpy as np
import matplotlib.pyplot as plt
from First_imp import First_improvement
import pandas as pd
import datetime

def read_data():
    data = {}

    data['R'] = pd.read_csv(os.path.join('data', 'small-r.csv'), delimiter=';',header=None)
    data['Mu'] = pd.read_csv(os.path.join('data', 'small-mu.csv'), delimiter=';',header=None)
    return data


class AP():

    def __init__(self, data):
        self.R = data['R'][1].tolist()
        self.Mu = data['Mu'][1].tolist()
    
    def AP_IPL(self):

        I = [i for i in range(len(self.R))]
        
        model = gp.Model('AP_IPL')

        # Variables
        y = {}
        y_non_zero = {}
        
        for i in I:
            y[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "y[%s]" % i, lb=0)

        for i in I:
            y_non_zero[i] = model.addVar(vtype=GRB.BINARY)

        Y_constrain = {}

        for i in I:
            Y_constrain[i] = model.addConstr(
                y[i] <= y_non_zero[i]*y[0]*exp(self.Mu[i])
            )

        model.addConstr(y[0]+gp.quicksum(y[i] for i in I[1:]) == 1)
        
        # Then set the objective function
        model.setObjective(self.R[0]*y[0] + gp.quicksum(self.R[i]*y[i] for i in I[1:]), GRB.MAXIMIZE)
        # Update the model
        model.update()

        # Otpimize it
        model.optimize()
        print("Optimization on AP-IPL is done. Objective function Value: %.2f " % model.ObjVal)


        return model

    def AP_IP(self):

        I = [i for i in range(len(self.R))]
        
        model = gp.Model('AP_IP')

        # Variables
        x= {}

        # Introduce a new variable to allow division by non-constant
        z= {}
        
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

        I = [i for i in range(len(self.R))]
        
        model = gp.Model('AP_LD')

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
        I = [i for i in range(len(self.R))]
        
        model = gp.Model('AP_L')

        # Variables
        y = {}
        
        for i in I:
            y[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "y[%s]" % i, lb=0)

        Y_constrain = {}

        for i in I:
            Y_constrain[i] = model.addConstr(
                y[i] <= y[0]*exp(self.Mu[i])
            )

        model.addConstr(y[0]+gp.quicksum(y[i] for i in I[1:]) == 1) # Need to remove i=0
        
        # Then set the objective function
        model.setObjective(self.R[0]*y[0] + gp.quicksum(self.R[i]*y[i] for i in I[1:]), GRB.MAXIMIZE)
        # Update the model
        model.update()


        # Otpimize it
        model.optimize()
        print("Optimization on AP-L is done. Objective function Value: %.2f " % model.ObjVal)

        return model

    def APC_MILP(self):

        I = [i for i in range(len(self.R))]

        p = len(I)/5
        
        model = gp.Model('APC_MILP')

        # Variables
        y = {}
        z = {}
        
        for i in I:
            y[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "y[%s]" % i, lb=0)

        for i in I:
            z[i] = model.addVar(vtype=GRB.BINARY, name = "z[%s]" % i)

        # 4 Constraints
        Y_constrain = {}
        Z_constrain = {}

        for i in I:
            Y_constrain[i] = model.addConstr(
                y[i] <= y[0]*exp(self.Mu[i])
            )

        for i in I:
            Z_constrain[i] = model.addConstr(y[i] <= z[i])

        # Constrain
        model.addConstr(y[0]+gp.quicksum(y[i] for i in I[1:]) == 1)
        model.addConstr(gp.quicksum(z[i] for i in I[1:]) <= p )
        
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

    def test(self,objValue,result_algo):
         
        value_taken_MILP = self.APC_MILP()
        value_taken_L= self.AP_L()
        value_taken_LD= self.AP_LD()
        value_taken_IP= self.AP_IP()
        value_taken_IPL= self.AP_IPL()
        # Retrieve the data from the CSV file, r => the net revenue of the object i where i belongs to I
        #                                      mu => the mean utilities of the object i

        # Ecris tous dans un fichier texte
        now = datetime.datetime.now()

        # Format the filename
        filename = 'test_file_{}.txt'.format(now.strftime("%Y%m%d%H%M%S"))

        with open(filename, 'w') as f:
            # Iterate over the variables
            f.write('AP-LD result -> obj_value {} selected item {} \n'.format(value_taken_LD.ObjVal,value_taken_LD.getAttr('X')))
            f.write('AP-IP result -> obj_value {} selected item {} \n'.format(value_taken_IP.ObjVal,value_taken_IP.getAttr('X')))
            f.write('AP-L result -> obj_value {} selected item {} \n'.format(value_taken_L.ObjVal,value_taken_L.getAttr('X')))
            f.write('AP-MILP result -> obj_value {} selected item {} \n'.format(value_taken_MILP.ObjVal,value_taken_MILP.getAttr('X')[:11]))
            f.write('AP-MILP result -> obj_value {} selected item {} \n'.format(value_taken_IPL.ObjVal,value_taken_IPL.getAttr('X')[:11]))
            f.write('Polynomial algo result -> obj_value {} selected item {} \n'.format(objValue,result_algo))

data = read_data()

# Extract a column's data into a list
# Print the list
polynomial_algo = First_improvement(data['R'][1],data['Mu'][1])
Problem_Ap = AP(data=data)
Problem_Ap.test(polynomial_algo[1],polynomial_algo[0])
# print(First_improvement(data['R'][1],data['Mu'][1]))
# model_AP_MILP = Problem_Ap.APC_MILP()
# print(model_AP_MILP.getAttr('X')[:11])
# model_AP_L= Problem_Ap.AP_L()
# print(model_AP_L.getAttr('X'))
# model_AP_LD= Problem_Ap.AP_LD()
# print(model_AP_LD.getAttr('X'))
# for v in model_AP_LD.getVars():
#     print(f"{v.VarName} = {v.X}")
# print(model_AP_LD.getAttr('X'))
# model_AP_IP= Problem_Ap.AP_IP()
# print(model_AP_IP.getAttr('X'))
# print([j.X for j in model_AP_IP.getVars()])
# for v in model_AP_IP.getVars():
#     print(f"{v.VarName} = {v.X}")
# model_AP_IPL= Problem_Ap.AP_IPL()
# print(model_AP_IPL.getAttr('X'))
# names_to_retrieve = (f"y[{i}]" for i in range(len(data['R'])))
# y_value = [model_AP_IPL.getVarByName(name).X for name in names_to_retrieve]
# print(y_value)