import unittest
from queue.tasksqueue import TasksQueue
from queue.itaskcallback import ITaskCallback

from hamcrest import *
from mockito import verify
from mockito import when
from mockito import mock
from mockito import unstub
from mockito.matchers import any , Matcher


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.Q = TasksQueue()
        self.callback = mock(ITaskCallback)

    def tearDown(self):
        self.Q.stop()

    def test_execution_order(self):
        when(self.callback).call(any(str), any(int)).\
            thenReturn(True)

        self.Q.push_tasks("TEST", [1*n for n in range(1, 6)], self.callback.call)
        self.Q.push_tasks("TEST2", [1*n for n in range(1, 6)], self.callback.call)

        self.Q.wait()
        self.Q.stop()

        assert_that(self.Q.empty(), equal_to(True))

        verify(self.callback, inorder=1).call("TEST", 1)
        verify(self.callback, inorder=1).call("TEST", 3)
        verify(self.callback, inorder=1).call("TEST", 2)
        verify(self.callback, inorder=1).call("TEST", 4)
        verify(self.callback, inorder=1).call("TEST", 5)

        verify(self.callback, inorder=1).call("TEST2", 1)
        verify(self.callback, inorder=1).call("TEST2", 2)
        verify(self.callback, inorder=1).call("TEST2", 3)
        verify(self.callback, inorder=1).call("TEST2", 4)
        verify(self.callback, inorder=1).call("TEST2", 5)


if __name__ == "__main__":
    unittest.main()
