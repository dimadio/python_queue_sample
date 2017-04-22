import unittest
from queue.tasksqueue import TasksQueue
from queue.itaskcallback import ITaskCallback

from hamcrest import *
from mockito import verify
from mockito import when
from mockito import mock
from mockito import unstub
from mockito.matchers import any, Matcher

import time
from threading import Thread

class TestCallback(ITaskCallback):
    def __init__(self):
        self.timestamps = dict()

    def call(self, user, wait):
        now = time.time()
        self.timestamps[user] = now


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.Q = TasksQueue()
        self.callback = TestCallback()

    def tearDown(self):
        self.Q.stop()

    def test_execution_order(self):
        self.Q.push_tasks("TEST", [10*n for n in range(1, 6)], self.callback.call)
        self.Q.push_tasks("TEST2", [1*n for n in range(1, 6)], self.callback.call)

        self.Q.wait()
        self.Q.stop()

        assert_that(self.Q.empty(), equal_to(True))

        assert_that(self.callback.timestamps, has_key("TEST"))
        assert_that(self.callback.timestamps, has_key("TEST2"))
        assert_that(self.callback.timestamps["TEST"], less_than(self.callback.timestamps["TEST2"]))


class TestMultiClients(unittest.TestCase):
    TheQueue = None
    clients = None
    clients_num = 10
    callback = None
    ready = False

    @classmethod
    def setUpClass(cls):
        cls.callback = TestCallback()
        cls.TheQueue = TasksQueue()

        cls.clients = [Thread(name="client_%d" % index,
                              target=cls.client_runner,
                              kwargs=dict(client_name="TEST_%d" % index))
                       for index in xrange(0, cls.clients_num)]

    @classmethod
    def client_runner(cls, client_name):
        cls.TheQueue.push_tasks(client_name, [10*n for n in range(1, 6)], cls.callback.call)

    def test_multi(self):

        for client in TestMultiClients.clients:
            ## We run add from different thread
            client.start()

        TestMultiClients.TheQueue.wait()
        TestMultiClients.TheQueue.stop()

        for index in xrange(0, TestMultiClients.clients_num):
            assert_that(self.callback.timestamps, has_key("TEST_%d" % index))

        for index in xrange(1, TestMultiClients.clients_num):
            assert_that(self.callback.timestamps["TEST_%d" % (index-1)], 
                    less_than(self.callback.timestamps["TEST_%d" % index]))
        
if __name__ == "__main__":
    unittest.main()
