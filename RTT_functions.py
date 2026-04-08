
def compute_od_to_downstream_TT(T, K, odl_keys, OD_route, link_tt, lengths):
    tt = {}
    for k in K:
        for (o,d,l) in odl_keys:
            tt_sum = 0
            current_time = k
            current_step = k
            for l_traverse in OD_route[o,d]:
                if current_step <= K[-1]:
                    remain_dist = lengths[l_traverse]
                    link_tt_current = link_tt[l_traverse,current_step]
                    if (current_time + link_tt_current) > (current_step + T) and (current_step + T) <= K[-1]:
                        remain_time = (current_step + T) - current_time
                        link_speed_current = lengths[l_traverse] / link_tt_current
                        remain_dist = remain_dist - remain_time * link_speed_current
                        tt_sum += remain_time
                        current_time += remain_time
                        current_step += T
                        while remain_dist > 0:
                            if current_step <= K[-1]:
                                link_speed_current = lengths[l_traverse] / link_tt[l_traverse,current_step]
                                if remain_dist > T * link_speed_current:
                                    tt_sum += T
                                    remain_dist = remain_dist - T * link_speed_current
                                    current_step += T
                                    current_time += T
                                else:
                                    tt_sum += remain_dist / link_speed_current
                                    current_time += remain_dist / link_speed_current
                                    remain_dist = 0
                            else:
                                tt_sum = 99999
                                break
                    elif (current_time + link_tt_current) > (current_step + T) and (current_step + T) > K[-1]:
                        tt_sum = 99999
                        break
                    else:
                        tt_sum += link_tt_current
                        current_time += link_tt_current
                else:
                    tt_sum = 99999
                    break
                if l_traverse == l:
                    break
            tt[o,d,l,k] = round(tt_sum,0)
    return tt

def compute_od_to_upstream_TT(T, K, odl_keys, OD_route, link_tt, lengths):
    tt = {}
    for k in K:
        for (o,d,l) in odl_keys:
            tt_sum = 0
            current_time = k
            current_step = k
            for l_traverse in OD_route[o,d]:
                if l_traverse == l:
                    break
                if current_step <= K[-1]:
                    remain_dist = lengths[l_traverse]
                    link_tt_current = link_tt[l_traverse,current_step]
                    if (current_time + link_tt_current) > (current_step + T) and (current_step + T) <= K[-1]:
                        remain_time = (current_step + T) - current_time
                        link_speed_current = lengths[l_traverse] / link_tt_current
                        remain_dist = remain_dist - remain_time * link_speed_current
                        tt_sum += remain_time
                        current_time += remain_time
                        current_step += T
                        while remain_dist > 0:
                            if current_step <= K[-1]:
                                link_speed_current = lengths[l_traverse] / link_tt[l_traverse, current_step]
                                if remain_dist > T * link_speed_current:
                                    tt_sum += T
                                    remain_dist = remain_dist - T * link_speed_current
                                    current_step += T
                                    current_time += T
                                else:
                                    tt_sum += remain_dist / link_speed_current
                                    current_time += remain_dist / link_speed_current
                                    remain_dist = 0
                            else:
                                tt_sum = 99999
                                break
                    elif (current_time + link_tt_current) > (current_step + T) and (current_step + T) > K[-1]:
                        tt_sum = 99999
                        break
                    else:
                        tt_sum += link_tt_current
                        current_time += link_tt_current
                else:
                    tt_sum = 99999
                    break
            tt[o,d,l,k] = round(tt_sum,0)
    return tt
