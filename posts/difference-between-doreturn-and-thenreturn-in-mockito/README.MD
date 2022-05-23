
# Difference between `doReturn` and `thenReturn` in Mockito

Two ways to mock the result of a method:
1. Use `doReturn` followed by `when`
1. Use `when` followed by `thenReturn`

## Use `doReturn` followed by `when`

Notice that `getByName` method is called __after__ the `when` method.

```java
@Test
public void test() {
    Cat cat = new Cat();
    cat.setName('Tom');
    CatServiceImpl catService = new CatServiceImpl();

    // `doReturn` followed by `when`
    // Note that `getByName` is called after`when`
    doReturn(cat).when(catService).getByName(any());

    Cat result = catService.getByName('Tom');
    assertEquals('Tom', result.getName());
}
```

## Use `when` followed by `thenReturn`

Notice that `getByName` method is called __within__ the `when` method.

```java
@Test
public void test() {
    Mouse mouse = new Mouse();
    mouse.setName('Jerry');
    MouseServiceImpl mouseService = new MouseServiceImpl();

    // `when` followed by `thenReturn`
    // Note that `getByName` is called within `when`
    when(mouseService.getByName(any()).thenReturn(mouse);

    Mouse result = mouseService.getByName('Jerry');
    assertEquals('Jerry', result.getName());
}
```
