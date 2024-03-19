from flask import request, g
from time import time
from functools import wraps
from typing import Callable, Dict, Set, Tuple
from werkzeug.exceptions import TooManyRequests

class RateLimiter:
    def __init__(self, max_requests: int, window_size: int):
        if max_requests <= 0:
            raise ValueError("max_requests must be a positive integer")
        if window_size <= 0:
            raise ValueError("window_size must be a positive integer")

        self.max_requests = max_requests
        self.window_size = window_size
        self.access_records: Dict[str, Set[float]] = {}

    def is_allowed(self, user_id: str) -> bool:
        current_time = time()
        window_start = current_time - self.window_size

        # Clean old records outside of the current window
        if user_id in self.access_records:
            self.access_records[user_id] = {timestamp for timestamp in self.access_records[user_id] if timestamp > window_start}
        else:
            self.access_records[user_id] = set()

        # Check if the user is allowed to make a request
        if len(self.access_records[user_id]) < self.max_requests:
            self.access_records[user_id].add(current_time)
            return True
        else:
            return False

def rate_limit(max_requests: int, window_size: int) -> Callable[[Callable], Callable]:
    limiter = RateLimiter(max_requests, window_size)

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapped(*args, **kwargs) -> Tuple[Any
