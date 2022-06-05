
# Implementing A Service That Toggles Between Cache And Database

## Overview

1. Model
1. Data Access Object
1. Service

## Model

```python
from dataclasses import dataclass

@dataclass
class Person:
    """ Person class. """
    id: str
    first_name: str
    last_name: str

```

## Data Access Object

Data Access Object (DAO) is an abstract light object to provide connection to the datastore (e.g. cache, database).

We define an abstract `PersonDao` class which will be inherited by a database and cache class.

__PersonDao__

```python
from abc import ABC

class PersonDao(ABC):

    def connect(self):
        pass

    def get(self, id):
        pass

```

__PersonDbDao__

PersonDbDao connects to a database and performs SQL queries.

```python
import mysql.connector

class PersonDbDao(PersonDao):

    def __init__(self):
        self.cursor = self.connect()

    def connect(self):
        db = mysql.connector.connect(
            host = "localhost",
            user = "username",
            password = "passoword"
        )
        return db.cursor()

    def get(self, key):
        query = f"SELECT * FROM PERSON WHERE ID = '{key}'"
        self.cursor.execute(query)
        return self.cursor.fetchone()

```

__PersonCacheDao__

PersonCacheDao connects to a cache and performs `get` and `put` operations.

```python
from pymemcache.client import base

class PersonCacheDao(PersonDao):

    def __init__(self):
        self.client = self.connect()

    def connect(self):
        client = base.Client(('localhost', 11211))
        return client

    def get(self, key):
        return self.client.get(key)

```

## Service

The server layer provides logic to operate on the data sent to and from the DAO and client. For security reasons, this layer should not have any relation to the database or cache.

We define a PersonService interface with an abtract method `get` which must be implemented by the implementing class.

__PersonServiceInterface__:

```python
from abc import ABC

class PersonServiceInterface(ABC):

    @abstractmethod
    def get(self, id):
        """ Get person by id. """
        pass

```

__PersonServiceImpl__:

PersonServiceImpl implements PersonServiceInterface:

1. A `use_db` flag is used to determine whether to perform the operation on the database or cache.
1. When using cache, we should also handle cache-miss scenarios by looking up the entry from database and putting it into cache.

```python
class PersonServiceImpl(PersonServiceInterface):

    def __init__(self):
        self.use_db = False
        self.db = PersonDbDao()
        self.cache = PersonCacheDao()

    def get(self, key):
        value = None
        if self.use_db:
            value = self.db.get(key)
        else:
            value = self.cache.get(key)
            if value is None:
                value = self.db.get(key)
                if not self.cache.put(key, value):
                    logging.error('Cache add failed.')
        return value

```

## CacheMiss

### Caveats

1. Cache is volatile
1. Cache is not transactional
1. Cache is a limited resource

### Cache Is Volatile

Because cache is volatile, entries can be evicted anytime by various reasons:

1. entry reached expiration
1. entry is evicted because cache memory is full
1. cache server fails

Hence:

1. Important to handle cache-miss gracefully
1. Implement write-through logic by backing cache with datastore in your application

### Cache Is Not Transactional

1. Use `getIdentifiable()` and `putIfUntouched()` for optimistic locking

### Cache Is A Limit Resource

1. Cache only what is useful and necessary
1. Your application should function without cache

### Handling Cache-Miss During `Get`

If entry is not found in cache then:

1. Fetch entry from database
1. Put entry into cache

```python
from google.appengine.api import memcache

value = memcache.get(key)

if value is None:
    value = get_value_from_db(key)
        if not memcache.add(key, value):
            logging.error('Memcache add failed.')

```
