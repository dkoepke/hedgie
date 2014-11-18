Hedgie
======

Hedgie is a library for building fault and latency tolerant distributed systems in Python. Hedgie provides:

1. A function decorator, `hedgie.command`, for easily wrapping service calls to provide a fallback implementation in the event the service call fails.
2. A [circuit breaker](http://martinfowler.com/bliki/CircuitBreaker.html) that prevents cascading failure in decorated service calls by automatically using the fallback when Hedgie detects the service call's error rate or average response time is outside of acceptable parameters.
3. An easy way to isolate service calls leveraging `concurrent.futures`. Service calls may be synchronously or asynchronously.

# Installation and Quick Start

Install Hedgie using pip:

    pip install hedgie

To use Hedgie, take an existing function that makes a service call and wrap it with the `hedgie.command` decorator. Consider the following very simple service function using [requests](http://python-requests.org):

```python
import requests

def get_json_service(url):
    return requests.get(url).json()

result = get_json_service('http://example.org')
print(result)
```

This method can fail in several ways: the URL given can be invalid; the service at that URL may be unavailable or have an error; or the response might not be valid JSON. With this typical implementation of a service call, the caller must take care to handle these errors. As is, if any of these problems occur, our simple example will exit with an error.

With Hedgie, we can wrap the service call to provide a fallback so that errors are handled and a fallback mechanism is executed:

```python
import requests
import hedgie

def get_json_service_fallback(cmd, exc):
    return {'error': 'ServiceUnavailableError'}

@hedgie.command(fallback=get_json_service_fallback)
def get_json_service(url):
    return requests.get(url).json()

result = get_json_service('http://example.org')
print(result)
```

Note that we haven't changed the body of `get_json_service` or how it's called. We've simply wrapped the existing function with `hedgie.command` to point to our new fallback function.
