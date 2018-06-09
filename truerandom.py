from urllib.request import urlretrieve
import time
from argcheck import arg_check_type, arg_check_in
from threading import Thread

BASE_2 = 0x02
BASE_6 = 0x06
BASE_8 = 0x08
BASE_10 = 0x0A
BASE_16 = 0x10


def Get(min, max, count=1, base=BASE_10):
    arg_check_type((min, max), (int, int))
    base = arg_check_in(base, (BASE_2, BASE_6, BASE_8, BASE_10, BASE_16))
    if count < 1:
        return
    data = urlretrieve("https://www.random.org/integers/?num=%d&min=%d&max=%d&col=1&base=%d&format=plain&rnd=new" % (count, min, max, base))
    f = open(data[0], "r")
    data = f.readlines()

    result = []
    for i in data:
        i.replace('\n', '')
        result.append(int(i, base))
    if count > 1:
        return tuple(result)
    else:
        return result[0]
        
        
    

def RandomInteger(min, max, count=1, kwargs={}):
    pass

def DebugLatency(count=10, text=False):
    start = 0
    avg_lat = 0
    for i in range(0, count):
        start = time.time()
        Get(**kwargs)
        diff = time.time() - start
        avg_lat += diff
        if text:
            print(str(diff) + 's')

    avg_lat /= count
    if text:
        print("Average latency of: " + str(avg_lat) + "s")
    return avg_lat

_maxCount = 1000
_index = 0
_running = False

def nextInt():
    global _index
    global _currentVals
    if not _running:
        return None
    val = _currentVals[_index]
    _index += 1
    return val

def stopGenerator():
    global _running
    _running = False
    

def _randThread():
    global _running
    global _currentVals

    _currentVals = list(Get(0, 100, count=_maxCount))
    _running = True
    while _running:
        if _index > _maxCount / 2:
            newVals = list(Get(0, 100, count=_maxCount))
            _currentVals.reverse()
            for i in range(0, int(_maxCount / 2) - 1):
                _currentVals.pop()
            _currentVals.reverse()
            _currentVals = newVals
        time.sleep(0.05)

_rand_thread = Thread(target=_randThread)
_rand_thread.start()
del _randThread
del _rand_thread
            
