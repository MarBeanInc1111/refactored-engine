from flask import request, g
from time import time
from functools import wraps
from werkzeug.exceptions import TooManyRequests

class RateLimiter:
    def __init__(self, max_requests, window_size):
        self.max_requests = max_requests
        self.window_size = window_size
        self.access_records = {}

    def is_allowed(self, user_id):
        current_time = time()
        window_start = current_time - self.window_size

        # Clean old records outside of the current window
        if user_id in self.access_records:
            self.access_records[user_id] = [timestamp for timestamp in self.access_records[user_id] if timestamp > window_start]
        else:
            self.access_records[user_id] = []

        # Check if the user is allowed to make a request
        if len(self.access_records[user_id]) < self.max_requests:
            self.access_records[user_id].append(current_time)
            return True
        else:
            return False

def rate_limit(max_requests, window_size):
    limiter = RateLimiter(max_requests, window_size)

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = g.user_id  # Assuming user_id is stored in Flask's global object 'g'
            if not limiter.is_allowed(user_id):
                raise TooManyRequests('You have exceeded the maximum number of requests. Please try again later.')
            return f(*args, **kwargs)
        return wrapped
    return decorator