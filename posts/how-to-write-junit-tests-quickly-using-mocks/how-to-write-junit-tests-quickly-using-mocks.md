
# How to write JUnit tests quickly using mocks

## Steps

1. Writing test for the class `Store.java`
1. Initialize an instance of `Store` in your test class
1. Use `@InjectMocks` on `Store` and `@Mock` on the member variables
1. Writing the test for `getCashiers()`
1. Run tests

### Writing test for the class `Store.java`

Consider a new class `Store.java` that we have written and we want to test the `getCashiers()` method:

```java
/* Store.java */
public class Store() {

  private String id;

  @Autowired
  private CashierServiceImpl cashierService;

  public Store(String id) {
    this.id = id;
  }

  public Cashiers[] getCashiers() throws CacheException {
    return cashierService.getByStoreId(this.id);
  }
}
```

We start by creating `StoreTest.java` which would contain our JUnit tests:

```java
/* StoreTest.java */
@RunWith(SpringJUnit4ClassRunner.class)
public class StoreTest() {
  // TODO
}
```

### Initialize an instance of `Store`

We first need to initialize an instance of `Store`. There are multiple ways that this can be done:
1. Manually initialize
1. Use `@Autowired`
1. Use `@InjectMocks` and `@Mocks`

#### Manually initializing

```java
@RunWith(SpringJUnit4ClassRunner.class)
public void StoreTest() {

  Store store;

  public StoreTest() {
    this.store = new Store("Cheers");
  }

}
```

The issue with manually initializing is that you may not be able to initialize the private member variables of `Store`:
1. `Store` does not take in an instance of `CashierServiceImpl` in its constructor
1. `CashierServiceImpl` is a private member variable which was initialized by Spring's dependency injection using `@Autowired`
1. As such, there is no way of initializing `CashierServiceImpl` manually in order to test the `getCashiers()` method as `CashierServiceImpl` is null

#### Using `@Autowired`

Well you may then consider annotating `Store` with `Autowired` instead and let Spring do its own dependency injection magic (however it works because we don't really care, do we..?):

```java
@RunWith(SpringJUnit4ClassRunner.class)
public void StoreTest() {

  @Autowired
  Store store;

}
```

Unfortunately,  you see such errors in your console log when you try to run `StoreTest`:
```log

```

Resolving these errors may or may not be straightforward.

### Use `@InjectMocks` and `@Mock`

Hence, one solution is to mock `Store` and its member variables:

```java
@RunWith(SpringJUnit4ClassRunner.class)
public class HelloWorldTest() {

  @InjectMocks
  Store store;

  @Mock
  CashierServiceImpl cashierService;

  @Before
  public void initMocks() {
    MockitoAnnotations.initMocks(this);
  }

}
```

### Run tests

