import hedgie


def hello_fallback(command):
    return 'fallback'


@hedgie.command(fallback=hello_fallback)
def hello(name, should_fail):
    """Say hello."""
    assert should_fail is False
    return 'Hello, {0}'.format(name)


def test_hello_should_pass_naive_introspection():
    assert hello.__module__ == hello_fallback.__module__
    assert hello.__name__ == 'hello'
    assert hello.__doc__ == 'Say hello.'


def test_hello_should_be_a_hedgie_command():
    assert isinstance(hello, hedgie.Command)


def test_hello_should_return_greeting_if_not_should_fail_when_called():
    result = hello('world', False)
    assert result == 'Hello, world'


def test_hello_should_return_fallback_if_should_fail_when_called():
    result = hello('world', True)
    assert result == 'fallback'
