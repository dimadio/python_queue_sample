from time import sleep
DEFAULT_WAIT = 0.001


class Task(object):
    """
    Sample task object.
    all the objective of call method is
    to wait a requied number of milliseconds
    """
    def __init__(self, User, wait=None, callback = None):
        self.user = User
        self.wait = wait if wait else DEFAULT_WAIT
        self.callback = callback 

    def __repr__(self):
        return "[Task] for User `%s` for %s" % (self.user, self.wait)

    def __call__(self):
        if self.callback:
            # print "call ",self.callback, "for ",self.user, self.wait
            self.callback(self.user, self.wait)
        sleep(self.wait / 1000.0)
        return self.wait

