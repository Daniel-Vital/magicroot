from datetime import datetime as dt


def time_function(func):
    """
    Decorator to time functions
    :param func: function to time execution
    :return: Decorated function
    """
    def wrapper(*args, **kwargs):
        begin = dt.now()
        rv = func(*args, **kwargs)
        time = dt.now() - begin
        print(f'\nMagicRoot - time_function: Function {func.__name__} took {time} to run')
        return rv

    return wrapper

