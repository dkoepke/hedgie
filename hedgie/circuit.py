class CircuitOpenException(Exception):
    pass


class CircuitBreaker(object):
    """A circuit breaker that trips when failure rate exceeds a threshold.

    """

    def __init__(self, failure_rate_threshold=0.5):
        super(CircuitBreaker, self).__init__()
        self.failure_rate_threshold = failure_rate_threshold
        self.calls = 0
        self.errors = 0

    @property
    def failure_rate(self):
        return float(self.errors) / self.calls if self.calls else 0.0

    @property
    def is_open(self):
        return self.failure_rate >= self.failure_rate_threshold

    def reset(self):
        self.calls = 0
        self.errors = 0

    def call(self, exc):
        if self.is_open:
            raise CircuitOpenException()

        self.calls += 1

        if exc is not None:
            self.errors += 1
