import logging as log

log.getLogger('magicroot.smartowl.sorter').addHandler(log.NullHandler())


class Sorter:
    """
    This class is used to sort elements into categories
    In practice it creates the framework to transform sets into dictionaries
    """
    def __init__(self, unsorted):
        """
        It saves the unsorted items, creates a variable for the sorted data and a counter for the reviewed elements
        :param unsorted: a set of unsorted items
        """
        self._unsorted_data = unsorted
        self._sorted_data = {}
        self._reviewed = 0

    def unsorted(self, *args, **kwargs):
        """
        This function will return unsorted elements in no specified order.
        Note that this function, is prepared, and expects for the unsorted data to be changed during the iteration,
        if this happens it will simply restart the draw of unsorted elements.
        :return: an iterator to the unsorted elements
        """
        try:
            while self._should_review(*args, **kwargs):
                current_sprint = self._unsorted_data.copy()
                for elem in current_sprint:
                    try:
                        self._should_review(current_sprint, *args, **kwargs)
                    except StopIteration:
                        break
                    self._reviewed += 1
                    log.debug(f'({self._reviewed} / {self.to_sort}) Reviewing unsorted {elem}')
                    yield elem
                    # if elem not in self.already_retrieved_without_sort:
        except StopIteration:
            pass

    def _should_review(self, current_sprint=None, unlimited=False):
        """
        This function evaluates if the unsorted engine should keep drawing items or stop the iteration
        :param current_sprint: current queue of elements to be reviewed
        :param unlimited: bool that defines if unsorted should always keep drawing items (default false)
        :return: True if unsorted should keep drawing, false otherwise
        """
        if unlimited:
            return True
        if len(self._unsorted_data) == 0:
            raise StopIteration
        if self._reviewed > self.to_sort:
            raise StopIteration
        if current_sprint is not None and current_sprint != self._unsorted_data:
            raise StopIteration
        return True

    @property
    def to_sort(self):
        """
        :return: the number of elements to sort
        """
        return len(self._unsorted_data)

    def sort(self, elem, bucket):
        """
        This function moves an element from the unsorted set to the sorted dictionary, along with the appropriate
        bucket
        :param elem: element to the sorted
        :param bucket: 
        :return:
        """
        self._reviewed = 0
        self._create_bucket_if_missing(bucket)
        self._unsorted_data.remove(elem)
        self._sorted_data[bucket].append(elem)
        log.debug(f'Sorted {elem} into bucket: {bucket}')

    def _create_bucket_if_missing(self, bucket):
        if bucket not in self._sorted_data.keys():
            self._sorted_data[bucket] = []


