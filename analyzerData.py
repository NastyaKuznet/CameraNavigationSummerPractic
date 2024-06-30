
def compare_trajectories(x1, y1, times1, times2):
    good = []
    bad = []
    flag = False
    for i1 in range(len(times1)):
        for i2 in range(len(times2)):
            if times1[i1] == times2[i2]:
                flag = True
                break
        if flag:
            good.append((x1[i1], y1[i1]))
        else:
            bad.append((x1[i1], y1[i1]))
    return len(bad) == 0, good, bad


