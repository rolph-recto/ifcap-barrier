import random
import time
import threading

# threading.Barrier seems to unblock threads in LIFO order
# so this wrapper inserts random delays to prevent that
class RandomBarrier(threading.Barrier):
    DELAY_BOUND = 0.01

    def __init__(self, n):
        super().__init__(n)

    def wait(self):
        super().wait()
        time.sleep(random.random() * RandomBarrier.DELAY_BOUND)

barrier = RandomBarrier(2)
lock = threading.Lock()

hi = True
lo = True

def f1():
    global lo
    if hi:
        time.sleep(0.5)

    barrier.wait()
    with lock:
        lo = True

def f2():
    global lo
    time.sleep(0.1)

    barrier.wait()
    with lock:
        lo = False

t1 = threading.Thread(target=f1)
t2 = threading.Thread(target=f2)

t2.start()
t1.start()

t1.join()
t2.join()

print(lo)

