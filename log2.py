import array

log2_tab=array.array('B')

def init_log2():
    log2_tab.append(0)
    for i in range(8):
        for j in range (2**i):
            log2_tab.append(i+1)

def log2(i):
    return log2_tab[i]
