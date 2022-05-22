
# How to write JUnit tests using @InjectMocks and @Mocks

## Steps

1. Create the test file
1. Initialize an instance of the class to test using `@InjectMocks` and `@Mock`
1. Write the JUnit test method
1. Run the test 

### Create the test file

Consider a new class `Store.java` that we have written and we want to test the `getMaleCashiers()` method:

```java
/* src/Store.java */
public class Store() {

  private String id;

  @Autowired
  private CashierServiceImpl cashierService;

  public Store(String id) {
    this.id = id;
  }

  public List<Cashier> getMaleCashiers() throws CacheException {
    List<Cashier> cashierList = cashierService.getByStoreId(this.id);
    return cashierList.stream().filter(c -> c.getGender().equalsIgnoreCase('male')).collect(Collectors.toList()));
  }
}
```

Note that 'Store' has a private member variable 'CashierServiceImpl' which is initialized through Spring's dependency injection framework using @Autowired.

We start by creating `StoreTest.java` which will contain our JUnit test. The test class is annotated with @RunWith(SpringJUnit4ClassRunner.class):

```java
/* test/StoreTest.java */
@RunWith(SpringJUnit4ClassRunner.class)
public class StoreTest() {
  // TODO: Initialize objects
  // TODO: Write test cases
}
```

### Initialize an instance of the class to test using `@InjectMocks` and `@Mock`

We declare the member variables Store and CashierServiceImpl in the test class.

By annotating 'store' with @InjectMocks and cashierServiceImpl with @Mock, store will have a mock instance of cashierServiceImpl when store is initialized instead of being null.

Finally, we also need to call 'MockitAnnotations.initMocks(this);' to initialize the mock variables before the tests are run. One way to do this is by calling initMocks() in a method (e.g. initMocks()) annotated with @Before:

```java
/* test/StoreTest.java */
@RunWith(SpringJUnit4ClassRunner.class)
public class StoreTest() {

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

### Write the JUnit test method

```java
/* test/StoreTest.java */
@RunWith(SpringJUnit4ClassRunner.class)
public class StoreTest() {

  //...
  
  @Test
  public void getMaleCashiersTest() throws Cache exception {
    // CashierList with one male and one female cashier
    List<Cashier> cashierList = new ArrayList<>();
    
    Cashier maleCashier = new Cashier();
    maleCashier.setGender("male");
    cashierList.add(maleCashier);
    
    Cashier femaleCashier = new Cashier();
    femaleCashier.setGender(“female”);
    cashierList.add(femaleCashier);
    
    // Mock the getByStoreId method 
when(cashier Service.getByStoreId(any())).thenReturn(cashierList);

    // Test and assert
    List<Cashier> result = store.getMaleCashiers();
     assertEquals(1, result.size());
  }

}
```

### Other ways to initialize the `Store` instance

In the above example, we have seen how we can initialize Store using `@InjectMocks` and `@Mocks`.

There are also other ways that this can be done:
1. Manually initialize
1. Using `@Autowired`

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