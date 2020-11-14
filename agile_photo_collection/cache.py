import typing as t
from collections import defaultdict


class DictBasedCache:
    def __init__(
        self, pk_field: str, index_keys: t.Union[t.List[str], t.Tuple[str, ...]]
    ):
        self._documents = {}
        self._index = defaultdict(lambda: defaultdict(list))
        self.pk_field = pk_field
        self.index_keys = index_keys

    def index(self, document: dict):
        self._documents[document[self.pk_field]] = document
        for key_field in self.index_keys:
            if key_field not in document:
                continue
            if not isinstance(document[key_field], list):
                self._index[key_field][document[key_field]].append(
                    document[self.pk_field]
                )
            else:
                # one exceptional case: if key is a list - we should make an index for all keys in list,
                # to make ability to search by any of the elements
                for item in document[key_field]:
                    self._index[key_field][item].append(document[self.pk_field])

    def get_by_index(self, key):
        result = set()
        for key_field in self.index_keys:
            if (
                key in self._index[key_field]
            ):  # that means we have documents with given query
                result.update(self._index[key_field][key])

        return [self._documents[pk] for pk in result]
