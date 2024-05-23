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
import time

def read_data(size):
    data = {}

    data['R'] = pd.read_csv(os.path.join('data', f'{size}-r.csv'), delimiter=';',header=None)
    data['Mu'] = pd.read_csv(os.path.join('data', f'{size}-mu.csv'), delimiter=';',header=None)
    return data

class Result:
    def __init__(self):
        self.maximum = 0
        self.minimum = 1
        self.average = 0
        self.maximum_t = 0
        self.minimum_t = 600
        self.average_t = 0
    
    def set_parameter(self,result, time):
        if result > self.maximum:
            self.maximum = result
        if result < self.minimum:
            self.minimum = result
        self.average += result

        if time > self.maximum_t:
            self.maximum_t = time
        if time < self.minimum_t:
            self.minimum_t = time
        self.average_t += time

    def get_parameter(self):
        return self.minimum,self.maximum, self.average/100, self.minimum_t,self.maximum_t, self.average_t/100
        
    


class AP():

    def __init__(self, data,size):
        self.R = data['R'][1].tolist()
        self.Mu = data['Mu'][1].tolist()
        self.size = size
    
    def AP_IPL(self):

        I = [i for i in range(len(self.R))]
        
        model = gp.Model('AP_IPL')
        model.setParam('OutputFlag', 0)

        # Variables
        y = {}
        y_non_zero = {}
        
        for i in I:
            y[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "y[%s]" % i, lb=0)

        for i in I[1:]:
            y_non_zero[i] = model.addVar(vtype=GRB.BINARY)

        Y_constrain = {}

        for i in I[1:]:
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

    def APC_IP(self, p):

        I = [i for i in range(len(self.R))]
        
        model = gp.Model('AP_IP')
        model.setParam('OutputFlag', 0)

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
        
        model.addConstr(gp.quicksum(x[i] for i in I[1:]) <= p )

        model.setObjective((self.R[0] + gp.quicksum(x[i]*self.R[i]*exp(self.Mu[i]) for i in I[1:]))*z, GRB.MAXIMIZE)
        # Update the model
        model.update()


        # Otpimize it
        model.optimize()
        print("Optimization on AP-IP is done. Objective function Value: %.2f " % model.ObjVal)

        return model
    
    def AP_IP(self):

        I = [i for i in range(len(self.R))]
        
        model = gp.Model('AP_IP')
        model.setParam('OutputFlag', 0)

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
        model.setParam('OutputFlag', 0)

        # Variables
        pi = {}
        
        for i in I[1:]:
            pi[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "pi[%s]" % i, lb=0)

        pi_zero = model.addVar(vtype=GRB.CONTINUOUS, name="pi_zero")

        Pi_constrain = {}
        Pi_zero_constrain = {}

        for i in I:
            Pi_constrain[i] = model.addConstr(
                pi_zero - gp.quicksum(pi[i]*exp(self.Mu[i]) for i in I[1:]) >= self.R[0]
            )

        for i in I[1:]:
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
        model.setParam('OutputFlag', 0)

        # Variables
        y = {}
        
        for i in I:
            y[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "y[%s]" % i, lb=0)

        Y_constrain = {}

        for i in I[1:]:
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

    def APC_MILP(self,p):

        I = [i for i in range(len(self.R))]
        
        model = gp.Model('APC_MILP')
        model.setParam('OutputFlag', 0)

        # Variables
        y = {}
        z = {}
        
        for i in I:
            y[i] = model.addVar(vtype=GRB.CONTINUOUS, name = "y[%s]" % i, lb=0)

        for i in I:
            z[i] = model.addVar(vtype=GRB.BINARY, name = "z[%s]" % i)

        Y_constrain = {}
        Z_constrain = {}

        for i in I[1:]:
            Y_constrain[i] = model.addConstr(
                y[i] <= y[0]*exp(self.Mu[i])
            )

        for i in I[1:]:
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

        return model

    def test(self,objValue,result_algo, p):

        size = len(self.R)
         
        value_taken_MILP = self.APC_MILP(p)
        print("APC_MILP finished")
        value_taken_L= self.AP_L()
        print("AP_L finished")
        value_taken_LD= self.AP_LD()
        print("AP_LD finished")
        value_taken_IP= self.AP_IP()
        print("AP_IP finished")
        value_taken_IPL= self.AP_IPL()
        print("AP_IPL finished")
        value_taken_APC_IP=self.APC_IP(p)
        print("APC_IP finished")
        # Retrieve the data from the CSV file, r => the net revenue of the object i where i belongs to I
        #                                      mu => the mean utilities of the object i

        # Ecris tous dans un fichier texte
        now = datetime.datetime.now()

        # Format the filename
        filename = 'test_file_{}_{}.txt'.format(size,now.strftime("%d_%H_%M_%S"))
        # return pi[1] and finish with pi_zero that we minimize
        list_LD = [value_taken_LD.getAttr('X').index(j)+1 for j in value_taken_LD.getAttr('X')[:-2] if j > 0]
        # IP start with x[1] and finish with c10..
        list_IP = [j+1 for j in range(size-1) if value_taken_IP.getAttr('X')[j] > 0]
        # list_L return y[0] with its probababilty but we just want the taken object, so we start at 1
        list_L = [value_taken_L.getAttr('X').index(j) for j in value_taken_L.getAttr('X')[1:] if j > 0]
        # the output of getAttr gives a list composed of x list and another variable called C10
        # we thus take j+1 to inform about the taken object and not the index
        list_APC_IP = [j+1 for j in range(size-1) if value_taken_APC_IP.getAttr('X')[j] > 0]
        # contains the y and z value, with both y[0] and z[0] so we start at index 1
        list_MILP = [j for j in range(1,size-1) if value_taken_MILP.getAttr('X')[j] > 0]
        # list_IPL return y[0] with its probababilty but we just want the taken object, so we start at 1
        list_IPL = [j for j in range(1,size-1) if value_taken_IPL.getAttr('X')[j] > 0]


        with open(filename, 'w') as f:
            # Iterate over the variables
            f.write('AP-LD result -> obj_value {} \t\t selected item {} \n'.format(round(value_taken_LD.ObjVal,4),list_LD))
            f.write('AP-IP result -> obj_value {} \t\t selected item {} \n'.format(round(value_taken_IP.ObjVal,4),list_IP))
            f.write('AP-L result -> obj_value {} \t\t selected item {} \n'.format(round(value_taken_L.ObjVal,4),list_L))
            f.write('APC-IP result -> obj_value {} \t\t selected item {} \n'.format(round(value_taken_APC_IP.ObjVal,4),list_APC_IP))
            f.write('AP-MILP result -> obj_value {} \t\t selected item {} \n'.format(round(value_taken_MILP.ObjVal,4),list_MILP))
            f.write('AP-IPL result -> obj_value {} \t\t selected item {} \n'.format(round(value_taken_IPL.ObjVal,4),list_IPL))
            f.write('Polynomial algo result -> obj_value {} \t\t selected item {} \n'.format(round(objValue,4),result_algo))
    
    def test_csv(self,p,data):
        # index 0:minimum, index 1:maximum, index 2:average
        result_MILP = Result()
        result_L = Result()
        result_LD = Result()
        result_IP = Result()
        result_IPL = Result()
        result_C_IP = Result()
        result_poly = Result()

        for instance in range(100):
            print("Start instance",instance)
            self.R = data["R"][instance].tolist()
            self.Mu = data["Mu"][instance].tolist()

            start_time = time.time()
            AP_MILP=self.APC_MILP(p).ObjVal
            end_MILP = time.time()-start_time

            start_time = time.time()
            AP_L=self.AP_L().ObjVal
            end_AP_L = time.time()-start_time

            start_time = time.time()
            AP_LD=self.AP_LD().ObjVal
            end_AP_LD = time.time()-start_time

            start_time = time.time()
            AP_IP=self.AP_IP().ObjVal
            end_AP_IP = time.time()-start_time

            start_time = time.time()
            AP_IPL=self.AP_IPL().ObjVal
            end_AP_IPL = time.time()-start_time
            
            start_time = time.time()
            APC_IP=self.APC_IP(p).ObjVal
            end_APC_IP = time.time()-start_time

            start_time = time.time()
            poly=First_improvement(data["Mu"][instance],data["R"][instance])[1]
            end_poly = time.time()-start_time

            result_MILP.set_parameter(AP_MILP,end_MILP)
            result_L.set_parameter(AP_L,end_AP_L)
            result_LD.set_parameter(AP_LD,end_AP_LD)
            result_IP.set_parameter(AP_IP,end_AP_IP)
            result_IPL.set_parameter(AP_IPL,end_AP_IPL)
            result_C_IP.set_parameter(APC_IP,end_APC_IP)
            result_poly.set_parameter(poly,end_poly)

        # Create a dictionary with column names as keys and lists as values
        data = {
            'Model': ['Minimum', 'Maximum','Average', 'Minimum_time', "Maximum_time", "Average_time"],
            'AP-MILP': result_MILP.get_parameter(),
            'AP-L': result_L.get_parameter(),
            'AP-LD': result_LD.get_parameter(),
            'AP-IP':result_IP.get_parameter(),
            'AP-IPL':result_IPL.get_parameter(),
            'APC-IP':result_C_IP.get_parameter(),
            'Polynomial':result_poly.get_parameter()
        }

        # Convert the dictionary to a DataFrame
        df = pd.DataFrame(data)

        # Write the DataFrame to a CSV file
        df.to_csv(f'Test_instances_{self.size}.csv', index=False)

    def test_instances(self, p, data):

        list_MILP = []
        list_L = []
        list_LD = []
        list_IP = []
        list_IPL = []
        list_C_IP = []
        list_poly = []
        
        # for instance in range(100):
        instance=1
        self.R = data["R"][instance].tolist()
        self.Mu = data["Mu"][instance].tolist()
        list_MILP.append(self.APC_MILP(p).ObjVal)
        list_L.append(self.AP_L().ObjVal)
        list_LD.append(self.AP_LD().ObjVal)
        list_IP.append(self.AP_IP().ObjVal)
        list_IPL.append(self.AP_IPL().ObjVal)
        list_C_IP.append(self.APC_IP(p).ObjVal)
        list_poly.append(First_improvement(data["Mu"][instance],data["R"][instance])[1])

        # Retrieve the data from the CSV file, r => the net revenue of the object i where i belongs to I
        #                                      mu => the mean utilities of the object i

        # Ecris tous dans un fichier texte
        now = datetime.datetime.now()

        # Format the filename
        filename = 'plot_{}_{}.png'.format(len(data["R"][0]),now.strftime("%d_%H_%M_%S"))
        x = [j for j in range(1)]

        plt.figure(figsize=(12, 8))

        plt.plot(x,list_MILP, label='AP-MILP', marker='o')
        plt.plot(x, list_L, label='AP-L', marker='s')
        plt.plot(x, list_LD, label='AP-LD', marker='^')
        plt.plot(x, list_IP, label='AP-IP', marker='D')
        plt.plot(x, list_IPL, label='AP-IPL', marker='v')
        plt.plot(x, list_C_IP, label='APC-IP', marker='*')
        plt.plot(x, list_poly, label='Polynomial algo', marker='p')

        # Adding title and labels
        plt.title(f'Objective value of the models on {len(data["R"])}')
        plt.xlabel('Instance number')
        plt.ylabel('Objective value')

        # Adding a legend
        plt.legend()

        # Display the plot
        plt.grid(True)
        plt.show()
        # plt.savefig(filename)
