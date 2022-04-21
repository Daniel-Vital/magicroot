import logging as log
from .sorter import Sorter

log.getLogger('magicroot.smartowl.partiallyorderedset').addHandler(log.NullHandler())


class PartiallyOrderedSet(Sorter):
    """
    Partially Ordered Set (Mathematical concept) structure
    """
    def __init__(self, data):
        self._order = {}
        Sorter.__init__(self, data)
        self._new_next_order()

    def __str__(self):
        return self._sorted_data.__str__()

    def _new_next_order(self):
        for pair in self._computable_order():
            elem, prev_elem = pair
            order = self._compute_order(prev_elem)
            self.sort(pair, order)

    def _computable_order(self):
        for elem, prev_order_elem in self.unsorted():
            if prev_order_elem is None:  # so order 1
                log.debug(f'{elem} is of first order')
                yield elem, prev_order_elem

            elif prev_order_elem in self._computed_elements():
                log.debug(f'{elem} is of higher order')
                yield elem, prev_order_elem

    def _computed_elements(self):
        return (elem[0] for elems in self._sorted_data.values() for elem in elems)

    def _compute_order(self, prev_elem):
        for order, elems in self._sorted_data.items():
            if prev_elem in elems:
                return order + 1
        return 1

