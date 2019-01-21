# jsonslicer - stream JSON parser

<a href="https://repology.org/metapackage/python:jsonslicer/versions">
	<img src="https://repology.org/badge/vertical-allrepos/python:jsonslicer.svg" alt="jsonslicer packaging status" align="right">
</a>

[![Build Status](https://travis-ci.org/AMDmi3/jsonslicer.svg?branch=master)](https://travis-ci.org/AMDmi3/jsonslicer)
[![Coverage Status](https://coveralls.io/repos/github/AMDmi3/jsonslicer/badge.svg?branch=master)](https://coveralls.io/github/AMDmi3/jsonslicer?branch=master)
[![PyPI downloads](https://img.shields.io/pypi/dm/jsonslicer.svg)](https://pypi.org/project/jsonslicer/)
[![PyPI version](https://img.shields.io/pypi/v/jsonslicer.svg)](https://pypi.org/project/jsonslicer/)
[![PyPI pythons](https://img.shields.io/pypi/pyversions/jsonslicer.svg)](https://pypi.org/project/jsonslicer/)

## Overview

JsonSlicer performs a **stream** or **iterative** JSON parsing,
which means it **does not load** whole JSON into memory and is able
to parse **very large** JSON files or streams. The module is written
in C and uses [YAJL](https://lloyd.github.io/yajl/) JSON parsing
library, so it's also quite **fast**.

JsonSlicer takes a **path** of JSON map keys or array indexes, and provides
**iterator interface** which yields JSON data matching given path as complete
Python objects.

## Example

```json
{
    "friends": [
        {"name": "John", "age": 31},
        {"name": "Ivan", "age": 26}
    ],
    "colleagues": {
        "manager": {"name": "Jack", "age": 33},
        "subordinate": {"name": "Lucy", "age": 21}
    }
}
```

```python
from jsonslicer import JsonSlicer

# Extract specific elements:
with open('people.json') as data:
    ivans_age = next(JsonSlicer(data, ('friends', 1, 'age')))
	# 26

with open('people.json') as data:
    managers_name = next(JsonSlicer(data, ('colleagues', 'manager', 'name')))
	# 'Jack'

# Iterate over collection(s) by using wildcards in the path:
with open('people.json') as data:
    for person in JsonSlicer(data, ('friends', None)):
        print(person)
        # {'name': 'John', 'age': 31}
        # {'name': 'Ivan', 'age': 26}

# Iteration over both arrays and dicts is possible, even at the same time
with open('people.json') as data:
    for person in JsonSlicer(data, (None, None)):
        print(person)
        # {'name': 'John', 'age': 31}
        # {'name': 'Ivan', 'age': 26}
        # {'name': 'Jack', 'age': 33}
        # {'name': 'Lucy', 'age': 21}

# Map key of returned objects is available on demand...
with open('people.json') as data:
    for position, person in JsonSlicer(data, ('colleagues', None), path_mode='map_keys'):
        print(position, person)
        # 'manager' {'name': 'Jack', 'age': 33}
        # 'subordinate' {'name': 'Lucy', 'age': 21}

# ...as well as complete path information
with open('people.json') as data:
    for person in JsonSlicer(data, (None, None), path_format='full'):
        print(person)
        # ('friends', 0, {'name': 'John', 'age': 31})
        # ('friends', 1, {'name': 'Ivan', 'age': 26})
        # ('colleagues', 'manager', {'name': 'Jack', 'age': 33})
        # ('colleagues', 'subordinate', {'name': 'Lucy', 'age': 21})

# Extract all instances of deep nested field
with open('people.json') as data:
    age_sum = sum(JsonSlicer(data, (None, None, 'age')))
    # 111
```

## API

```
jsonslicer.JsonSlicer(
	file,
	path_prefix,
	read_size=1024,
	path_mode=None,
	yajl_allow_comments=False,
	yajl_dont_validate_strings=False,
	yajl_allow_trailing_garbage=False,
	yajl_allow_multiple_values=False,
	yajl_allow_partial_values=False,
	encoding=None,
	errors=None,
	binary=False,
)
```

Constructs iterative JSON parser which reads JSON data from _file_ (a `.read()`-supporting [file-like object](https://docs.python.org/3/glossary.html#term-file-like-object) containing a JSON document).

_path_prefix_ is an iterable (usually a list or a tuple) specifying
a path or a path pattern of objects which the parser should extract
from JSON.

For instance, in the example above a path `('friends', 0, 'name')`
will yield string `'John'`, by descending from the root element
into the dictionary element by key `'friends'`, then into the array
element by index `0`, then into the dictionary element by key
`'name'`. Note that integers only match array indexes and strings
only match dictionary keys.

The path can be turned into a pattern by specifying `None` as a
placeholder in some path positions. For instance,  `(None, None,
'name')` will yield all four names from the example above, because
it matches an item under 'name' key on the second nesting level of
any arrays or map structure.

_read_size_ is a size of block read by the parser at a time.

_path_mode_ is a string which specifies how a parser should
return path information along with objects. The following modes are
supported:

* _'ignore'_ (the default) - do not output any path information, just
objects as is (`'friends'`).

  ```python
  {'name': 'John', 'age': 31}
  {'name': 'Ivan', 'age': 26}
  {'name': 'Jack', 'age': 33}
  {'name': 'Lucy', 'age': 21}
  ```

  Common usage pattern for this mode is

  ```python
  for object in JsonWriter(...)
  ```

* _'map_keys'_ - output objects as is when traversing arrays and tuples
consisting of map key and object when traversing maps.

  ```python
  {'name': 'John', 'age': 31}
  {'name': 'Ivan', 'age': 26}
  ('manager', {'name': 'Jack', 'age': 33})
  ('subordinate', {'name': 'Lucy', 'age': 21})
  ```

  This format may seem inconsistent (and therefore it's not the default),
  however in practice only collection of a single type is iterated at
  a time and this type is known, so this format is likely the most useful
  as in most cases you do need dictionary keys.

  Common usage pattern for this mode is

  ```python
  for object in JsonSlicer(...)  # when iterating arrays
  for key object in JsonSlicer(...)  # when iterating maps
  ```

* _'full_paths'_ - output tuples consisting of all path components
(both map keys and array indexes) and an object as the last element.

  ```python
  ('friends', 0, {'name': 'John', 'age': 31})
  ('friends', 1, {'name': 'Ivan', 'age': 26})
  ('colleagues', 'manager', {'name': 'Jack', 'age': 33})
  ('colleagues', 'subordinate', {'name': 'Lucy', 'age': 21})
  ```

  Common usage pattern for this mode is

  ```python
  for *path, object in JsonWriter(...)
  ```

_yajl_allow_comments_ enables corresponding YAJL flag, which is
documented as follows:

> Ignore javascript style comments present in JSON input.  Non-standard,
> but rather fun

_yajl_dont_validate_strings_ enables corresponding YAJL flag, which
is documented as follows:

> When set the parser will verify that all strings in JSON input
> are valid UTF8 and will emit a parse error if this is not so.  When
> set, this option makes parsing slightly more expensive (~7% depending
> on processor and compiler in use)

_yajl_allow_trailing_garbage_ enables corresponding YAJL flag, which
is documented as follows:

> By default, yajl will ensure the entire input text was consumed
> and will raise an error otherwise.  Enabling this flag will cause
> yajl to disable this check.  This can be useful when parsing json
> out of a that contains more than a single JSON document.

_yajl_allow_multiple_values_ enables corresponding YAJL flag, which
is documented as follows:

> Allow multiple values to be parsed by a single handle.  The entire
> text must be valid JSON, and values can be seperated by any kind
> of whitespace.  This flag will change the behavior of the parser,
> and cause it continue parsing after a value is parsed, rather than
> transitioning into a complete state.  This option can be useful
> when parsing multiple values from an input stream.

_yajl_allow_partial_values_ enables corresponding YAJL flag, which
is documented as follows:

> When yajl_complete_parse() is called the parser will check that the
> top level value was completely consumed.  I.E., if called whilst
> in the middle of parsing a value yajl will enter an error state
> (premature EOF).  Setting this flag suppresses that check and the
> corresponding error.

_encoding_ may be used to override output encoding, which is derived
from the input file handle if possible, or otherwise set to the
default one as Python builttn `open()` would use (usually `'UTF-8'`).

_errors_ is an optional string that specifies how encoding and
decoding errors are to be handled. Defaults to `'strict'`

_binary_ forces the output to be in form of `bytes` objects instead
of `str` unicode strings.

The constructed object is as iterator. You may call `next()` to extract
single element from it, iterate it via `for` loop, or use it in generator
comprehensions or in any place where iterator is accepted.

## Performance/competitors

The closest competitor is [ijson](https://github.com/isagalaev/ijson),
and JsonSlicer was written to be better. Namely,

* It's about 15x faster, similar in performance to Python's native `json` module
* It allows iterating over dictionaries and allows more flexibility when
  specifying paths/patterns of objects to iterate over

The results of bundled benchmark on Python 3.7 / clang 6.0.1 / `-O2 -DNODEBUG` / FreeBSD 12.0 amd64 / Core i7-6600U CPU @ 2.60GHz.

| Facility                    | Type   | Objects/sec   |
|:----------------------------|:------:|--------------:|
| json.loads()                | str    | 1198.7K       |
| json.load(StringIO())       | str    | 1126.7K       |
| **JsonSlicer (no paths)**   | bytes  | 1195.2K       |
| **JsonSlicer (full paths)** | bytes  | 817.9K        |
| ijson.yajl2_cffi            | bytes  | 75.1K         |
| ijson.yajl2                 | bytes  | 52.4K         |
| ijson.python                | str    | 32.9K         |

## Status/TODO

JsonSlicer is currently in alpha stage, passing tests but pending
code safety checks and improvements. Also, the following mandatory
features are planned to be implemented to consider the module ready
to use:

- Allow to transparently operate on text I/O handles (in addition
  to bytes I/O) and return text data (instead of bytes) with specified
  encoding

## Requirements

- Python 3.6+
- pkg-config
- [yajl](https://lloyd.github.io/yajl/) JSON pasing library

## License

MIT license, copyright (c) 2019 Dmitry Marakasov amdmi3@amdmi3.ru.
