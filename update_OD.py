import xml.etree.ElementTree as ET
import pickle

from config import scenario, K, od_keys, odk_keys

directory = 'sumo_scenario'+scenario+'_repro/'

def read_OD(var_text):
    OD_dict = {}
    for (o,d,k) in odk_keys:
        OD_dict[o,d,k] = int(var_text['x['+o+','+d+','+repr(k)+']'])
    return OD_dict

def update_OD(OD):
    route_file = ET.parse(directory+'sioux_falls'+scenario+'_repro.rou_flow.xml')
    for item in route_file.getroot():
        if item.tag == 'flow':
            o_d = item.attrib['id'][2:].split('_')[0]  # ex:f_3-56_21600
            ori = o_d.split('to')[0]
            des = o_d.split('to')[1]
            interv = int(item.attrib['begin'])
            new_demand = OD[ori, des, interv]
            item.attrib['number'] = repr(new_demand)
    route_file.write(directory+'sioux_falls'+scenario+'_repro.rou_flow.xml')

with open('results'+scenario+'.pickle', 'rb') as handle:
    results_temp = pickle.load(handle)
Var = results_temp['Variable']
OD_opt = read_OD(Var)

OD_opt_all = {}
for (o,d) in od_keys:
    for k in K:
        if ((o,d,k) in OD_opt) == True:
            OD_opt_all[o,d,k] = OD_opt[o,d,k]
        else:
            OD_opt_all[o,d,k] = 0

update_OD(OD_opt_all)
