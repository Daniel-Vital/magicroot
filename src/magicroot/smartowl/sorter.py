import logging as log

log.getLogger('magicroot.smartowl.sorter').addHandler(log.NullHandler())


class Sorter:
    def __init__(self, unsorted):
        self._unsorted_data = unsorted
        self._sorted_data = {}
        self.already_retrieved_without_sort = []
        self._reviewed = 0

    def unsorted(self, *args, **kwargs):
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

                    if elem not in self.already_retrieved_without_sort:
                        self.already_retrieved_without_sort.append(elem)
                        yield elem
        except StopIteration:
            pass


    @property
    def to_sort(self):
        return len(self._unsorted_data)

    def _should_review(self, current_sprint=None, unlimited=False):
        if unlimited:
            return True
        if len(self._unsorted_data) == 0:
            raise StopIteration
        if self._reviewed > self.to_sort:
            raise StopIteration
        if current_sprint is not None and current_sprint != self._unsorted_data:
            raise StopIteration
        return True

    def sort(self, elem, bucket):
        self._reviewed = 0
        self.already_retrieved_without_sort = []
        self._create_bucket_if_missing(bucket)
        self._unsorted_data.remove(elem)
        self._sorted_data[bucket].append(elem)
        log.debug(f'Sorted {elem} into bucket: {bucket}')

    def _create_bucket_if_missing(self, bucket):
        if bucket not in self._sorted_data.keys():
            self._sorted_data[bucket] = []


