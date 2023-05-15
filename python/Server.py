import asyncio
from threading import Thread

from python.Optimizer import Optimizer

optimizer = Optimizer()


def run_local(idx, time):
    optimizer.solve(idx, seconds_limit=time)


t1 = Thread(target=run_local, args=[757, 10])
t2 = Thread(target=run_local, args=[756, 10])
# t3 = Thread(target=run_local, args=[757, 10])
t1.start()
t2.start()
# t3.start()
t1.join()
t2.join()
# t3.join()
# run_local(757, 10)
# run_local(757)
# run_local(757)
# asyncio.run(run_local(757))
