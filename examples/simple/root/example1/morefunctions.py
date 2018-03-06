from example1.myfunctions import debug_log


def sum_stuff(a, b):
    debug_log('SUM: {}+{}'.format(a, b))
    return a + b
