def compute_od_to_downstream_TT(T, K, odl_keys, OD_route, link_tt, lengths):
    tt = {} # in seconds
    for k in K:
        for (o,d,l) in odl_keys:
            tt_sum = 0
            current_time = k
            current_step = k
            for l_traverse in OD_route[o,d]:
                if current_step <= K[-1]:
                    remaining = lengths[l_traverse]
                    link_tt_temp = link_tt[l_traverse, current_step]
                    if (current_time + link_tt_temp) > (current_step + T) and (current_step + T) <= K[-1]:
                        remain_time = (current_step + T) - current_time
                        remaining = remaining - remain_time * (lengths[l_traverse] / link_tt[l_traverse, current_step])
                        tt_sum += remain_time
                        current_time += remain_time
                        current_step += T
                        while remaining > 0:
                            if current_step <= K[-1]:
                                if remaining > T * (lengths[l_traverse]/link_tt[l_traverse,current_step]):
                                    tt_sum += T
                                    remaining = remaining - T * (lengths[l_traverse]/link_tt[l_traverse,current_step])
                                    current_step += T
                                    current_time += T
                                else:
                                    tt_sum += remaining / (lengths[l_traverse]/link_tt[l_traverse,current_step])
                                    current_time += remaining / (lengths[l_traverse] / link_tt[l_traverse, current_step])
                                    remaining = 0
                            else:
                                tt_sum = 99999
                                current_step += T
                                break
                    elif (current_time + link_tt_temp) > (current_step + T) and (current_step + T) > K[-1]:
                        tt_sum = 99999
                        break
                    else:
                        if l_traverse == l:
                            tt_sum += link_tt[l_traverse,current_step]
                        else:
                            tt_sum += link_tt[l_traverse,current_step]
                            current_time += link_tt[l_traverse,current_step]
                else:
                    tt_sum = 99999
                    break
                if l_traverse == l:
                    break
            tt[o,d,l,k] = round(tt_sum,0)
    return tt

def compute_od_to_upstream_TT(T, K, odl_keys, OD_route, link_tt, lengths):
    tt = {} # in seconds
    for k in K:
        for (o,d,l) in odl_keys:
            tt_sum = 0
            l_index = OD_route[o,d].index(l)
            if l_index > 0:
                ul = OD_route[o,d][l_index-1]
                current_time = k
                current_step = k
                for l_traverse in OD_route[o,d]:
                    if current_step <= K[-1]:
                        remaining = lengths[l_traverse]
                        link_tt_temp = link_tt[l_traverse,current_step]
                        if (current_time + link_tt_temp) > (current_step + T) and (current_step + T) <= K[-1]:
                            remain_time = (current_step + T) - current_time
                            remaining = remaining - remain_time * (lengths[l_traverse] / link_tt[l_traverse, current_step])
                            tt_sum += remain_time
                            current_time += remain_time
                            current_step += T
                            while remaining > 0:
                                if current_step <= K[-1]:
                                    if remaining > T * (lengths[l_traverse]/link_tt[l_traverse,current_step]):
                                        tt_sum += T
                                        remaining = remaining - T * (lengths[l_traverse]/link_tt[l_traverse,current_step])
                                        current_step += T
                                        current_time += T
                                    else:
                                        tt_sum += remaining / (lengths[l_traverse]/link_tt[l_traverse,current_step])
                                        current_time += remaining / (lengths[l_traverse] / link_tt[l_traverse, current_step])
                                        remaining = 0
                                else:
                                    tt_sum = 99999
                                    current_step += T
                                    break
                        elif (current_time + link_tt_temp) > (current_step + T) and (current_step + T) > K[-1]:
                            tt_sum = 99999
                            break
                        else:
                            if l_traverse == ul:
                                tt_sum += link_tt[l_traverse,current_step]
                            else:
                                tt_sum += link_tt[l_traverse,current_step]
                                current_time += link_tt[l_traverse,current_step]
                    else:
                        tt_sum = 99999
                        break
                    if l_traverse == ul:
                        break
            tt[o,d,l,k] = round(tt_sum,0)
    return tt