import pickle

T = 900
K = [int(0 + i * T) for i in range(12)]
K_JAM = 133.33

with open('params/link_length.pickle', 'rb') as handle:
    link_length = pickle.load(handle)

# number of lanes of all links in the network
with open('params/all_lane_num.pickle', 'rb') as handle:
    lane_num = pickle.load(handle)

with open('params/link.pickle', 'rb') as handle:
    L = pickle.load(handle)

with open('params/o_keys.pickle', 'rb') as handle:
    o_keys = pickle.load(handle)

with open('params/od_keys.pickle', 'rb') as handle:
    od_keys = pickle.load(handle)

with open('params/odl_keys.pickle', 'rb') as handle:
    odl_keys = pickle.load(handle)

odk_keys = [(key[0],key[1],k) for key in od_keys for k in K]

lk_keys = [(l,k) for l in L for k in K]

with open('params/lk_evaluation_keys.pickle', 'rb') as handle:
    lk_evaluation_keys = pickle.load(handle)

with open('params/lk_entry_keys.pickle', 'rb') as handle:
    lk_entry_keys = pickle.load(handle)

scenario = '_uncon'
#scenario = '_con'

directory = 'sumo_scenario'+scenario+'/'

with open(directory+'OD_route.pickle', 'rb') as handle:
    OD_route = pickle.load(handle)

with open(directory+'link_count.pickle', 'rb') as handle:
    link_count = pickle.load(handle)

with open(directory+'link_den.pickle', 'rb') as handle:
    link_den = pickle.load(handle)

link_accum = {}
for (l,k) in lk_keys:
    link_accum[l,k] = link_den[l,k] / 1000 * link_length[l] * lane_num[l]

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
