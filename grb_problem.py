import os
import pickle
import gurobipy as gp
from gurobipy import GRB
from config import K, T, o_keys, odk_keys, lk_keys, odl_keys, lk_evaluation_keys, lk_entry_keys, link_length, lane_num, gamma

from count_function import calculate_count

#%% Gurobi license
parent_directory = os.path.dirname(os.path.dirname(__file__))
# Set the path to your license file
license_file_path = r"C:\gurobi1300\gurobi.lic" # check!
# Set the environment variable
os.environ["GRB_LICENSE_FILE"] = license_file_path

def save_results(model,scenario):
    results = {
        "Variable": {v.VarName: v.X for v in model.getVars()},
        "Objective": model.ObjVal
    }
    with open('results'+scenario+'.pickle', 'wb') as handle:
        pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)

def opt_model(scenario,tt_OD_to_downstream, tt_OD_to_upstream, l_count, l_den, q_entry, zeros, fc, fd, K_JAM):

    m = gp.Model()
    x = m.addVars(odk_keys, vtype=GRB.INTEGER, name="x", lb=0)  # OD demand every 15-min interval
    a = m.addVars(lk_evaluation_keys+lk_entry_keys, vtype=GRB.CONTINUOUS, name="a", lb=0)
    d_mid = m.addVars(lk_evaluation_keys+lk_entry_keys, vtype=GRB.CONTINUOUS, name="d_mid", lb=0)
    uc = m.addVars(lk_evaluation_keys, vtype=GRB.CONTINUOUS, name="uc")  # link count error every 15-min interval
    ud = m.addVars(lk_evaluation_keys+lk_entry_keys, vtype=GRB.CONTINUOUS, name="ud")  # link den error every 15-min interval
    ux = m.addVars(odk_keys, vtype=GRB.CONTINUOUS, name="ux", lb=0)

    # obj
    obj = gp.quicksum(uc[l,k]**2 for (l,k) in lk_evaluation_keys)
    obj += gp.quicksum(ud[l,k]**2 for (l,k) in lk_evaluation_keys)
    obj += gp.quicksum(gamma * ux[o,d,k] ** 2 for (o,d,k) in odk_keys)

    # inflow / count mapping
    q = calculate_count(T, tt_OD_to_upstream, K, lk_keys, odl_keys, x)

    # errors
    for (l,k) in lk_evaluation_keys:
        m.addConstr(uc[l,k] >= (l_count[l,k] - q[l,k]) / fc)
        m.addConstr(uc[l,k] >= - (l_count[l,k] - q[l,k]) / fc)
    for (l,k) in lk_evaluation_keys:
        m.addConstr(ud[l,k] >= (l_den[l,k] - d_mid[l,k]) / fd)
        m.addConstr(ud[l,k] >= - (l_den[l,k] - d_mid[l,k]) / fd)

    # demand spreading
    for (o,d,k) in odk_keys:
        m.addConstr(ux[o,d,k] >= (0 - x[o,d,k]) / q_entry[o,k])
        m.addConstr(ux[o,d,k] >= - (0 - x[o,d,k]) / q_entry[o,k])

    # intermediate accum
    for (l,k) in (lk_evaluation_keys+lk_entry_keys):
        if k == K[0]:
            m.addConstr(d_mid[l,k] == a[l,k] / 2 / (link_length[l]/1000) / lane_num[l])
        else:
            m.addConstr(d_mid[l,k] == (a[l,k-T] + a[l,k]) / 2 / (link_length[l]/1000) / lane_num[l])
    
    # outflow mapping
    g = calculate_count(T, tt_OD_to_downstream, K, lk_keys, odl_keys, x)
    
    # link accumulation update
    for (l,k) in (lk_evaluation_keys+lk_entry_keys):
        if k == K[0]:
            m.addConstr(a[l,k] == 0 + q[l,k] - g[l,k])
        else:
            m.addConstr(a[l,k] == a[l,k-T] + q[l,k] - g[l,k])
    
    # link accumulation constraint
    for (l,k) in (lk_evaluation_keys):
        m.addConstr(a[l,k] <= K_JAM/1000 * link_length[l] * lane_num[l])

    # inflow at origins
    for k in K:
        for o in o_keys: # each origin node
            m.addConstr(gp.quicksum(x[o_temp,d,k_temp] for (o_temp,d,k_temp) in odk_keys if (o == o_temp) and (k == k_temp)) == q_entry[o,k])

    # zero ODs
    for (o,d) in zeros:
        for k in K:
            m.addConstr(x[o,d,k] == 0)

    # problem setting
    m.setObjective(obj, GRB.MINIMIZE)
    m.write('m.lp')
    m.setParam('TimeLimit', 1 * 60 * 60)
    m.Params.LogToConsole = 1

    # execution
    m.optimize()
    save_results(m,scenario)
