from AP_problem import read_data, AP
from First_imp import First_improvement

data = read_data("small")

# Extract a column's data into a list
# Print the list
# polynomial_algo = First_improvement(data['Mu'][1],data['R'][1])
print("Algo poly finished")
Problem_Ap = AP(data=data, size="small")
Problem_Ap.test_csv(len(data['R'][0])-1,data)
# Problem_Ap.test(polynomial_algo[1],polynomial_algo[0], len(data['R'][1])-1)
# Problem_Ap.test_instances(1, data)
# print(First_improvement(data['R'][1],data['Mu'][1]))
# model_AP_MILP = Problem_Ap.APC_MILP(1)
# for v in model_AP_MILP.getVars():
#     print(f"{v.VarName} = {v.X}")
# model_AP_MILP = Problem_Ap.APC_MILP((len(data["R"][0])-1)/5)
# for v in model_AP_MILP.getVars():
#     print(f"{v.VarName} = {v.X}")
# model_AP_MILP = Problem_Ap.APC_MILP((len(data["R"][0])-1)/2)
# for v in model_AP_MILP.getVars():
#     print(f"{v.VarName} = {v.X}")
# model_AP_MILP = Problem_Ap.APC_MILP((len(data["R"][0])-1))
# for v in model_AP_MILP.getVars():
#     print(f"{v.VarName} = {v.X}")
# model_AP_L= Problem_Ap.AP_L()
# for v in model_AP_L.getVars():
#     print(f"{v.VarName} = {v.X}")
# model_AP_LD= Problem_Ap.AP_LD()
# for v in model_AP_LD.getVars():
#     print(f"{v.VarName} = {v.X}")
# model_AP_IP= Problem_Ap.AP_IP()
# for v in model_AP_IP.getVars():
#     print(f"{v.VarName} = {v.X}")
# model_AP_IPL= Problem_Ap.AP_IPL()
# for v in model_AP_IPL.getVars():
#     print(f"{v.VarName} = {v.X}")
# names_to_retrieve = (f"y[{i}]" for i in range(len(data['R'])))
# y_value = [model_AP_IPL.getVarByName(name).X for name in names_to_retrieve]
# print(y_value)
# model_APC_IP=Problem_Ap.APC_IP(len(data['R'][0]))
# print(model_APC_IP.getAttr('X'))
# for v in model_APC_IP.getVars():
#     print(f"{v.VarName} = {v.X}")