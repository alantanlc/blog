
# Implementing A Service That Toggles Between Cache And Database

## Overview

1. Model
1. Data Access Object
1. Service
1. CacheMiss

## Model

```python
class Person:

    def __init__(self):
        self.id = None
        self.first_name = None
        self.last_name = None

```

## Data Access Object

Data Access Object (DAO) is an abstract light object to provide connection to the datastore (e.g. cache, database).

__PersonDao__:
```python
class PersonDao:

    def __init__(self):
        self.source = self.connect()

    def connect(self):
        pass

    def get(self, id):
        pass

    def save(self, person):
        pass

    def put(self, person):
        pass

```

__PersonDbDao__:
```python
import mysql.connector

class PersonDbDao(PersonDao):

    def __init__(self):
        super.__init__()
        self.cursor = None

    def connect(self):
        source = mysql.connector.connect(
            host = "localhost",
            user = "username",
            password = "passoword"
        )
        self.cursor = db.cursor()
        return source

    def get(self, id):
        query = f"SELECT * FROM PERSON WHERE ID = '{id}'"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def save(self, person):
        query = f"INSERT INTO PERSON (first_name, last_name) VALUES ({person.first_name}, {person.last_name})"
        self.cursor.execute(query)
        self.source.commit()
        person.id = self.cursor.lastrowid
        return person

    def put(self, person):
        pass

```

__PersonCacheDao__:
```python
class PersonCacheDao(PersonDao):

    def __init__(self):
        pass

    def get(self, id):
        pass

    def save(self, person):
        pass

    def put(self, person):
        pass

```

## Service

Server layer provides logic to operate on the data sent to and from the DAO and client.

For security reaons, the service layer should not have any relation to the datastore.

__PersonServiceInterface__:

```python
class PersonServiceInterface:

    def __init__(self):
        self.use_db = False
        self.db = PersonDbDao()
        self.cache = PersonCacheDao()

    def use_db(self):
        return self.use_db

    def set_use_db(self, flag):
        self.use_db = flag

```

__PersonServiceImpl__:

```python
class PersonServiceImpl(PersonServiceInterface):

    def __init__(self):
        pass

    def get(self, id):
        if self.use_db():
            return self.db.get(id)
        else:
            return self.cache.get(id)

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
