from collections import namedtuple
import functools
import sys

from .circuit import CircuitBreaker, CircuitOpenException


class RuntimeException(Exception):
    pass


class OperationalException(Exception):
    def __init__(self, cause):
        super(OperationalException, self).__init__()
        self.cause = cause

    def reraise(self, exc_traceback):
        raise self.cause.__class__, self.cause, exc_traceback


_CommandInvocation = namedtuple(
    'CommandExecution',
    ('command', 'args', 'kwargs', 'exception'))


class CommandInvocation(_CommandInvocation):
    """Represents the invocation of a command.

    Attributes
    ----------
    command : Command
        The command that was invoked
    args : list
        The positional arguments passed when the command was invoked
    kwargs : mapping
        The keyword arguments passed when the command was invoked
    exception : Exception
        The exception, if any, that caused the invocation to terminate

    """
    pass


class Command(object):
    def __init__(self, service_call, group=None, fallback=None, circuit_breaker=None):
        super(Command, self).__init__()
        self.service_call = service_call
        self.group = group or get_qualname(service_call)
        self.fallback = fallback
        self.circuit_breaker = circuit_breaker or CircuitBreaker()

    def __call__(self, *args, **kwargs):
        # return self.queue(*args, **kwargs).result()
        try:
            if self.circuit_breaker.is_open:
                raise CircuitOpenException()

            result = self.service_call(*args, **kwargs)

            self.circuit_breaker.call(None)
            return result
        except OperationalException as exc:
            # Skip fallback and re-raise
            exc.reraise(sys.exc_info()[2])
        except Exception as exc:
            invocation = CommandInvocation(
                command=self, args=args, kwargs=kwargs, exception=exc)

            if not isinstance(exc, CircuitOpenException):
                self.circuit_breaker.call(exc)

            if self.fallback is not None:
                return self.fallback(invocation)

            raise  # No fallback, so we have to re-raise


def get_qualname(fn):
    if hasattr(fn, '__qualname__'):
        return fn.__qualname__

    module = None
    parts = []

    if hasattr(fn, '__module__'):
        module = fn.__module__
    elif hasattr(fn, '__class__'):
        module = fn.__class__.__module__
    elif hasattr(fn, 'im_class'):
        module = fn.im_class.__module__

    if module and module != str.__module__:
        parts.append(fn.__module__)

    if hasattr(fn, 'im_class'):
        parts.append(fn.im_class)

    parts.append(fn.__name__)

    return '.'.join(parts)


def command(group=None, fallback=None):
    """Provide latency and fault tolerance for service calls.

    Additional Arguments
    --------------------

    fallback: callable
        A callable that is invoked when the command fails. The callable is
        passed one argument, a :class:`CommandInvocation` that describes the
        invocation of the command.

    """

    def decorator(service_call):
        command = Command(service_call, group=group, fallback=fallback)
        functools.update_wrapper(command, service_call)
        return command

    return decorator
