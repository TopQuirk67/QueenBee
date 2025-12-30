import random
import time

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def recursive_waiter(t1=1.0,t2=3.0,t3=8.0,t4=10.0,phighbin=0.3,precursion=0.25,depth=None,maxdepth=None,scaler=1.0):
    '''
    t1...t4: wait times where t1<t2; t3<t4
    phighbin: probability of drawing a wait time from t3..t4
    precursion: probability of invoking an extra layer of recursion
    depth: passed to lower levels of recursion for stop condistion
    maxdepth: stop condition; if none, no recursion depth stop condition (not recommended!)
    scaler: a large number will speed up the process; wait times are divided by scaler; used mostly for debugging
    '''
    if depth:
        depth+=1
    else:
        depth=1
    if depth>maxdepth:
        return
    if random.random()>phighbin:
        sl = random.uniform(t1, t2)
        time.sleep(sl/scaler)
    else:
        sl = random.uniform(t3, t4)
        time.sleep(sl/scaler)
    if random.random()<precursion:
        recursive_waiter(t1,t2,t3,t4,phighbin,precursion,depth,maxdepth,scaler=scaler)

if __name__ == '__main__':
    pass