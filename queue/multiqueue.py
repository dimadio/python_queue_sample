from Queue import PriorityQueue, Empty
from time import time


class MultiQueue(object):
    """
    Simple priority queue interface to push/pull tasks
    Priority queue maintain the order by first element of the tuple, no futher ordering is guarantied
    """
    def __init__(self):
        self.queue = PriorityQueue()

    def empty(self):
        return self.queue.empty()

    def pull_nowait(self):
        task_data = self.queue.get_nowait()
        if task_data:
            (EnterTime, User, Task) = task_data
            self.queue.task_done()
            return (User, Task)

    def pull_wait(self, wait):
        try:
            task_data = self.queue.get(block=True, timeout=wait)
            (EnterTime, User, Task) = task_data
            self.queue.task_done()
            return (User, Task)
        except Empty:
            return None

    def push(self, User, Tasks):
        EnterTime = time()
        for task in Tasks:
            self.queue.put_nowait((EnterTime, User, task))
