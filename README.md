Hedgie
======

**This is a WIP**

Hedgie is a library for building fault (and, eventually, latency) tolerant distributed systems in Python. Hedgie provides:

1. A function decorator, `hedgie.command`, for easily wrapping service calls to provide a fallback implementation in the event the service call fails.
2. TODO: A [circuit breaker](http://martinfowler.com/bliki/CircuitBreaker.html) that prevents cascading failure in decorated service calls by automatically using the fallback when Hedgie detects the service call's error rate or average response time is outside of acceptable parameters.
3. TODO: An easy way to isolate service calls leveraging `concurrent.futures`. Service calls may be synchronously or asynchronously.

To understand the value that Hedgie provides, consider a function that makes an HTTP request and deserializes a JSON response. This service call can (and, given enough time, eventually will) fail in several ways: the URL given can be wrong; the service at that URL may be unavailable or have an error; the service may timeout in responding; or the response might be invalid. When building distributed systems, we implicitly expect callers to handle and isolate these errors in such a way to prevent cascading failure. In practice, few developers fully consider the failure modes of the service calls they're making and fragility creeps into every available crack.

# Installation and Quick Start

Install Hedgie using pip (TODO: not published on PyPI, yet):

    pip install hedgie

To use Hedgie, take an existing function that makes a service call and wrap it with the `hedgie.command` decorator. For example, consider the following (unrealistic) function:

```python
def hello_service(name, should_fail=False):
    if should_fail:
        raise Exception('intentionally failed')
    else:
        return 'Hello, {0}'.format(name)
```

We can add some degree of fault tolerance by defining a fallback function and decorating `hello_service` with `hedgie.command`:

```python
import hedgie


def hello_fallback(cmd):
    return 'Hello, world'


@hedgie.command(fallback=hello_fallback)
def hello_service(name, should_fail=False):
    if should_fail:
        raise Exception('intentionally failed')
    else:
        return 'Hello, {0}'.format(name)
```

The body of `hello_service` is exactly the same, but now when calling it:

```python
print(hello_service('Hedgie'), should_fail=False)  # => Hello, Hedgie
print(hello_service('Hedgie'), should_fail=True)   # => Hello, world
```

Without the `hedgie.command` decorator, the second line would cause the program to terminate with an unhandled exception.
