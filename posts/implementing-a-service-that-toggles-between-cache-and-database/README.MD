
# Implementing A Service That Toggles Between Cache And Database

## Overview

1. Model
1. Data Access Object
1. Service

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
