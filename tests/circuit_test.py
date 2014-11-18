import hedgie.circuit


def test_circuit_should_count_calls_and_failures():
    breaker = hedgie.circuit.CircuitBreaker(failure_rate_threshold=0.5)

    breaker.call(None)
    assert not breaker.is_open
    assert breaker.failure_rate == 0.0
    assert breaker.calls == 1

    breaker.call(None)
    assert not breaker.is_open
    assert breaker.failure_rate == 0.0
    assert breaker.calls == 2

    breaker.call(None)
    assert not breaker.is_open
    assert breaker.failure_rate == 0.0
    assert breaker.calls == 3

    breaker.call(Exception('1'))
    assert not breaker.is_open
    assert breaker.failure_rate == 1.0/4.0
    assert breaker.calls == 4

    breaker.call(Exception('2'))
    assert not breaker.is_open
    assert breaker.failure_rate == 2.0/5.0
    assert breaker.calls == 5

    breaker.call(Exception('3'))
    assert breaker.is_open
    assert breaker.failure_rate == 3.0/6.0
    assert breaker.calls == 6
