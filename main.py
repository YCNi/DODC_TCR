
import pickle
from RTT_functions import compute_od_to_upstream_TT
from RTT_functions import compute_od_to_downstream_TT
from grb_problem import opt_model

#scenario = '_con'
scenario = '_uncon'

directory = 'sumo_scenario'+scenario+'/'

T = 900
K = [int(0 + i * T) for i in range(12)]

with open(directory+'all_link_length.pickle', 'rb') as handle:
    all_link_length = pickle.load(handle)

# number of lanes of all links in the network
with open(directory+'all_lane_num.pickle', 'rb') as handle:
    all_lane_num = pickle.load(handle)

with open(directory+'link.pickle', 'rb') as handle:
    L = pickle.load(handle)

#%% key sets
with open(directory+'o_keys.pickle', 'rb') as handle:
    o_keys = pickle.load(handle)

with open(directory+'od_keys.pickle', 'rb') as handle:
    od_keys = pickle.load(handle)

with open(directory+'odl_keys.pickle', 'rb') as handle:
    odl_keys = pickle.load(handle)

odk_keys = [(key[0],key[1],k) for key in od_keys for k in K]
lk_keys = [(l,k) for l in L for k in K]

# evaluated ones
with open(directory+'lk_evaluation_keys.pickle', 'rb') as handle:
    lk_evaluation_keys = pickle.load(handle)

# entry ones
with open(directory+'lk_entry_keys.pickle', 'rb') as handle:
    lk_entry_keys = pickle.load(handle)

# all the links of each OD
with open(directory+'OD_route.pickle', 'rb') as handle:
    OD_route = pickle.load(handle)

with open(directory+'link_count.pickle', 'rb') as handle:
    link_count = pickle.load(handle)

with open(directory+'link_den.pickle', 'rb') as handle:
    link_den = pickle.load(handle)

link_accum = {}
for (l,k) in lk_keys:
    link_accum[l,k] = link_den[l,k] / 1000 * all_link_length[l] * all_lane_num[l]

with open(directory+'demand.pickle', 'rb') as handle:
    OD_sim = pickle.load(handle)

zero_OD = []
for (o,d) in od_keys:
    for k in K:
        if ((o,d,k) in OD_sim) == True:
            if OD_sim[o,d,k] != 0:
                break
            else:
                if k == K[-1]:
                    zero_OD.append((o, d))
        else:
            zero_OD.append((o, d))
            break

with open(directory+'inflow.pickle', 'rb') as handle:
    inflow = pickle.load(handle)

with open(directory+'link_TT.pickle', 'rb') as handle:
    link_TT = pickle.load(handle)

OD_to_downstream_TT = compute_od_to_downstream_TT(T, K, odl_keys, OD_route, link_TT, all_link_length)
OD_to_upstream_TT = compute_od_to_upstream_TT(T, K, odl_keys, OD_route, link_TT, all_link_length)

FC = max(link_count.values())
FD = max(link_den.values())
K_JAM = 133.33

opt_model(scenario,OD_to_downstream_TT,OD_to_upstream_TT,link_count,link_den,inflow,zero_OD,FC,FD,K_JAM)
