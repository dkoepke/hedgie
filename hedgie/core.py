from collections import namedtuple

from hedgie.circuit import CircuitBreaker, CircuitOpenException


class Command(object):
    """A command that tolerates faults and latency.

    """
    def __init__(self, service_call, group=None, fallback=None, circuit_breaker=None):
        super(Command, self).__init__()
        self.service_call = service_call
        self.group = group or get_qualname(service_call)
        self.fallback = fallback
        self.circuit_breaker = circuit_breaker or CircuitBreaker()

    def run(self):
        raise NotImplementedError('must implement Command.run method')

    def fallback(self, invocation):
        raise NotImplementedError('must implement Command.fallback method')

    def call(self, args, kwargs):
        if not self.circuit_breaker.allow_request:
            raise CircuitOpenException()

        result = self.run(*args, **kwargs)
        self.circuit_breaker.call(None)

        return result

    def handle_exception(self, exc, args, kwargs):
        invocation = CommandInvocation(command=self, args=args, kwargs=kwargs, exception=exc)
        self.circuit_breaker.call(exc)
        return self.fallback(invocation)

    def __call__(self, *args, **kwargs):
        # return self.queue(*args, **kwargs).result()
        try:
            return self.call(args, kwargs)
        except OperationalException as exc:
            # Propagate the wrapped exception
            exc.reraise(sys.exc_info()[2])
        except Exception as exc:
            return self.handle_exception(exc, args, kwargs)


class DecoratedCommand(Command):
    def __init__(self, service_call, fallback, group=None, circuit_breaker=None):
        super(DecoratedCommand, self).__init__()
        self.service_call = service_call
        self.fallback = fallback
        self.group = group or get_qualname(service_call)
        self.circuit_breaker = circuit.breaker_for_group(self.group)

    def run(self, *args, **kwargs):
        return self.service_call(*args, **kwargs)

    def fallback(self, invocation):
        return self.fallback(invocation)


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


class RuntimeException(Exception):
    pass


class OperationalException(Exception):
    def __init__(self, cause):
        super(OperationalException, self).__init__()
        self.cause = cause

    def reraise(self, exc_traceback):
        raise self.cause.__class__, self.cause, exc_traceback
