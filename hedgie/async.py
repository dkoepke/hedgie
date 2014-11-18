from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial
import multiprocessing
from Queue import Queue

from heading.core import CommandInvocation, OperationalException


DEFAULT_MAX_WORKER_THREADS = 10


def ThreadPoolExecutionStrategy(object):
    def __init__(self, max_workers=DEFAULT_MAX_WORKER_THREADS):
        super(ThreadPoolExecutionStrategy, self).__init__()
        self.q = Queue(maxsize=DEFAULT_MAX_WORKER_THREADS)

    def execute(self, command, args, kwargs):
        try:
            self.q.put((command, args, kwargs), block=False)
        except Queue.Full:
            exc = OperationalException(RuntimeError('Threads exhausted'))
            invocation = CommandInvocation(command=command, args=args, kwargs=kwargs, exception=)
            return command.fallback(invocation)



class Group(object):
    def __init__(self, name, circuit_breaker=None, execution_strategy=None):
        super(Group, self).__init__()
        self.name = name
        self.circuit_breaker = circuit_breaker
        self.executor_class = executor_class

    def queue(self, command):
        try:
            self.work_q.put(command, block=False)
        except
