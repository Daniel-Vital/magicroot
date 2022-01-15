
def print_file_head(path, nrows=10):
    """
    Prints the first rows (nrows) of a file (path)
    :param path: file to print
    :param nrows: number rows to print
    :return: None
    """
    with open(path) as file:
        head = [next(file) for _ in range(nrows)]
    print(head)
