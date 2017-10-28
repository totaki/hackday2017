"""
This class make dict as javascript object. Additional methods
help create from json, dumps to json, return as dict and update
Example:
    >>> attr_dict = AttrDict({'key1': {'key2': ['value1', 'value2']}})
    >>> attr_dict.key1.as_dict
    {'key2': ['value1', 'value2']}
    >>> attr_dict.key1.key2
    ['value1', 'value2']
    >>> attr_dict.key1.update({'key3': 'value4'})
    >>> attr_dict.key1.key3
    'value4'
    >>> attr_dict.key1.key2 = 'value3'
    >>> attr_dict.key1.key2
    'value3'
"""
import json


class AttrDict(object):

    aliases = {}

    def __init__(self, items):
        object.__setattr__(self, '_items', self._prepare_items(items))

    def __getattr__(self, item):
        return self._items.get(self.aliases.get(item, item), None)

    def __setattr__(self, key, value):
        if key in self._items.keys():
            self._items[self.aliases.get(key, key)] = value
        else:
            object.__setattr__(self, key, value)

    @staticmethod
    def _prepare_items(items):
        if hasattr(items, 'items'):
            items = items.items()
        return dict(
            (k, AttrDict(v)) if isinstance(v, dict) else (k, v)
            for k, v in items
        )

    @property
    def as_dict(self):
        return {
            k: v.as_dict if isinstance(v, AttrDict) else v
            for k, v in self._items.items()
        }

    @classmethod
    def from_json(cls, arg):
        if isinstance(arg, bytes):
            arg = arg.decode('utf-8')
        return cls(json.loads(arg))

    def to_json(self, encode=False):
        return json.dumps(self.as_dict).encode() if encode else json.dumps(self.as_dict)

    def update(self, items):
        self._items.update(self._prepare_items(items))


if __name__ == '__main__':
    import doctest
    doctest.testmod()