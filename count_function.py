import math

def calculate_count(T, tt_OD_to_link, K, lk_keys, odl_keys, X):
    count = {}
    for (l,k) in lk_keys:
        count[l,k] = 0
    for k in K:
        for (o,d,l) in odl_keys:
            portions = {}
            if k == K[0]:
                tt_head = tt_OD_to_link[o,d,l,k]
            else:
                tt_head = (tt_OD_to_link[o,d,l,k] + tt_OD_to_link[o,d,l,k-T]) / 2
            if k < K[-1]:
                tt_tail = (tt_OD_to_link[o,d,l,k] + tt_OD_to_link[o,d,l,k+T]) / 2
            else:
                tt_tail = tt_OD_to_link[o,d,l,k]
            arrival_head = k + tt_head
            arrival_tail = k + T + tt_tail
            head_interv = k + T * math.floor(tt_head/T)
            tail_interv = k + T + T * math.floor(tt_tail/T)
            if head_interv >= tail_interv:
                portions[head_interv] = 1
            else:
                num_interval = int((tail_interv - head_interv) / T) + 1
                packet_length = arrival_tail - arrival_head
                portions[head_interv] = (head_interv + T - arrival_head) / packet_length
                portions[tail_interv] = (arrival_tail - tail_interv) / packet_length
                for i in range(num_interval-2):
                    portions[head_interv+T*(i+1)] = T / packet_length
            for j in portions.keys():
                if (j in K) == True:
                    count[l,j] += X[o,d,k] * portions[j]
    return count
