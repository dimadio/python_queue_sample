from multiqueue import MultiQueue
from task import Task
from threading import Thread

class TasksQueue:
    """
    Queue and task wrapper
    Maintains required user/tasks interface
    and executes tasks in a BG thread. 
    """
    def __init__(self):
        self.queue = MultiQueue()
        self.running = True
        self.thread = Thread(name="manager", target=self._manage)
        self.thread.start()

    def push_tasks(self, User, delays, callback = None):
        Tasks = [Task(User, delay, callback) for delay in delays]
        self.queue.push(User, Tasks)

    def empty(self):
        return self.queue.empty()
    
    def wait(self):
        while not self.empty():
            self.thread.join(0.001)
        
    def join(self):
        while not self.empty():
            self.thread.join(0.001)
        self.stop()

    def stop(self):
        self.running = False
        self.thread.join()

    def _manage(self):
        while self.running:
            task_data = self.queue.pull_wait(1)
            if task_data:
                (User, task) = task_data
                ## print "run task ", task
                task()
