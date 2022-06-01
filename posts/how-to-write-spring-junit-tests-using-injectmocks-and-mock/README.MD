
# How to write Spring JUnit tests using @InjectMocks and @Mock

## Steps

1. Create the test file
1. Initialize an instance of the class to test using `@InjectMocks` and `@Mock`
1. Write the JUnit test method

## Create the test file

Consider a new class `Store.java` and we want to test the `getMaleCashiers()` method:

```java
/* Store.java */
public class Store() {

  private String id;

  @Autowired
  private CashierServiceImpl cashierService;

  public Store(String id) {
    this.id = id;
  }

  public List<Cashier> getMaleCashiers() throws CacheException {
    // Get list of cashiers by store id from cache or database
    List<Cashier> cashierList = cashierService.getByStoreId(this.id);
    
    // Filter and return list of male cashiers
    return cashierList
      .stream()
      .filter(c -> c.getGender().equalsIgnoreCase('male'))
      .collect(Collectors.toList()));
  }
}
```

Note that `Store` has a private member variable `CashierServiceImpl` which is initialized through Spring's dependency injection framework using `@Autowired`.

We start by creating `StoreTest.java` which will contain our JUnit test. The test class is annotated with `@RunWith(SpringJUnit4ClassRunner.class)`:

```java
/* StoreTest.java */
@RunWith(SpringJUnit4ClassRunner.class)
public class StoreTest() {
  // TODO: Initialize objects
  // TODO: Write test cases
}
```

## Initialize an instance of the class to test using `@InjectMocks` and `@Mock`

We declare the member variables `store` and `cashierServiceImpl` in the test class.

By annotating `store` with `@InjectMocks` and `cashierServiceImpl` with `@Mock`, `store` will have a mock instance of `cashierServiceImpl` instead of null.

Finally, we also need to call `MockitoAnnotations.initMocks(this)` to initialize the mock variables before the test is run. One way to do this is by calling it in a method annotated with `@Before`:

```java
/* StoreTest.java */
@RunWith(SpringJUnit4ClassRunner.class)
public class StoreTest() {

  @InjectMocks
  Store store;

  @Mock
  CashierServiceImpl cashierService;

  @Before
  public void initMocks() {
    // Initialize mock variables
    MockitoAnnotations.initMocks(this);
  }

}
```

## Write the JUnit test

Let's now write the test for the `store.getMaleCashiers()`. To recap:

```java
/* Store.java */
public class Store {
  // ...

  public List<Cashier> getMaleCashiers() throws CacheException {
    // Get list of cashiers by store id from cache or database
    List<Cashier> cashierList = cashierService.getByStoreId(this.id);
    
    // Return male cashiers
    return cashierList
      .stream()
      .filter(c -> c.getGender().equalsIgnoreCase('male'))
      .collect(Collectors.toList()));
  }

}
```

`cashierService.getByStoreId(this.id)` retrieves the list of cashiers associated with the given store id from either the cache or database.

For our test on `store.getMaleCashers()`:

1. we are not concerned with the underlying implementation of `cashierService.getByStoreId(this.id)`
1. `cashierService.getByStoreId(this.id)` does not need to retrieve the result from an actual cache or database when we run the test

As such, we can use Mockito's `when` and `thenReturn` methods to mock the result when `cashierService.getByStoreId(this.id)` is being called during testing.

What we _are_ concerned with is the following line that filters `cashierList` by male cashiers and returns the correct result.

As such, here we have the complete code for our test:

```java
/* StoreTest.java */
@RunWith(SpringJUnit4ClassRunner.class)
public class StoreTest() {

  @InjectMocks
  Store store;

  @Mock
  CashierServiceImpl cashierService;

  @Before
  public void initMocks() {
    // Initialize mock variables
    MockitoAnnotations.initMocks(this);
  }

  @Test
  public void getMaleCashiersTest_shouldReturnOne() throws CacheException {
    // CashierList
    List<Cashier> cashierList = new ArrayList<>();

    Cashier maleCashier = new Cashier();
    maleCashier.setGender("male");
    cashierList.add(maleCashier);

    Cashier femaleCashier = new Cashier();
    femaleCashier.setGender("female");
    cashierList.add(femaleCashier);

    // Mock getByStoreId(this.id) to return cashierList that we have created
    when(cashierService.getByStoreId(any())).thenReturn(cashierList);

    // Test and assert
    List<Cashier> result = store.getMaleCashiers();
    assertEquals(1, result.size());
  }
  
}
```

## Other ways to initialize the `Store` instance

In the above example, we have seen how we can initialize Store using `@InjectMocks` and `@Mocks`.

There are also other ways to initialize `Store` in the test class:

1. Manually initialize a `Store` instance
1. Use `@Autowired` on `store` member variable

### Manually initialize a `Store` instance

```java
@RunWith(SpringJUnit4ClassRunner.class)
public void StoreTest() {

  Store store;

  public StoreTest() {
    this.store = new Store("Cheers");
  }

  // @Test
  // ...

}
```

The issue with manually initializing is that you may not be able to initialize the private member variables of `Store`:

1. `Store` does not take in an instance of `CashierServiceImpl` in its constructor
1. `CashierServiceImpl` is a private member variable which is initialized by Spring's dependency injection framework using `@Autowired`

### Use `@Autowired` on `store` member variable

Well, you may then consider to annotate `Store` with `Autowired` instead and let Spring do its own dependency injection magic thingy. However it works because we don't really care...do we?

```java
@RunWith(SpringJUnit4ClassRunner.class)
public void StoreTest() {

  @Autowired
  Store store;

  // @Test
  // ...

}
```

Unfortunately, you see errors in your console log when you try to run `StoreTest`.

Resolving these errors may or may not be straightforward, depending on how complex the member variables are.
