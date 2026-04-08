import pickle
from RTT_functions import compute_od_to_upstream_TT
from RTT_functions import compute_od_to_downstream_TT
from grb_problem import opt_model
from config import odl_keys, link_length, T, K, K_JAM, OD_route, \
    scenario, link_TT, link_count, link_den, inflow, zero_OD, FC, FD

# calculate travel times
OD_to_downstream_TT = compute_od_to_downstream_TT(T, K, odl_keys, OD_route, link_TT, link_length)
OD_to_upstream_TT = compute_od_to_upstream_TT(T, K, odl_keys, OD_route, link_TT, link_length)

# execute optimization
opt_model(scenario,OD_to_downstream_TT,OD_to_upstream_TT,link_count,link_den,inflow,zero_OD,FC,FD,K_JAM)
