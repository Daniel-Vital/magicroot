from datetime import datetime as dt


def time_function(func):
    def wrapper(*args, **kwargs):
        begin = dt.now()
        rv = func(*args, **kwargs)
        time = dt.now() - begin
        print(f'function {func.__name__} took {time} to run')
        return rv

    return wrapper

