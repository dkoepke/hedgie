import functools

from hedgie.core import DecoratedCommand


def command(fallback, group=None):
    """Provide latency and fault tolerance for service calls.

    Arguments
    ---------

    fallback: callable
        A callable that is invoked when the command fails. The callable is
        passed one argument, a :class:`CommandInvocation` that describes the
        invocation of the command.

    Additional Arguments
    --------------------

    group: hedgie.async.Group
        The group that this command to. If not specified, a group is created
        with the fully-qualified name of the function pointed to by
        `service_call`.

    """

    def decorator(service_call):
        command = DecoratedCommand(service_call, fallback, group=group)
        functools.update_wrapper(command, service_call)
        return command

    return decorator
