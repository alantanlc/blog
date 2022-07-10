# Parsing Nested Data Structures

Parsing nested data structures can be tricky. This README shares multiple ways to parse complex objects along with the common pitfalls, pros and cons.

## Overview

1. [Nested data structure](#nested-data-structure)
1. [Chain of getters](#chain-of-getters)
1. [Concatenated null checks](#concatenated-null-checks)
1. [Optional](#optional)
1. [StatementHandler](#statementhandler)
1. [Nested null checks](#nested-null-checks)
1. [Flattened null checks](#flattened-null-checks) (Preferred method)

## Nested Data Structure

```java
class LevelOne {
  String levelOneName;
  LevelTwo levelTwo;
}

class LevelTwo {
  String levelTwoName;
  List<LevelThree> levelThreeList;
}

class LevelThree {
  String levelThreeName;
  Map<String, LevelFour> levelFourMap:
}

class LevelFour {
  String levelFourName;
}
``` 

## Chain Of Getters

While `levelFourName` can be retrieved using a chain of getters, this is an extremely bad way because __NullPointerException__ is thrown when one of the objects is null.

```java
public String getName(LevelOne levelOne) {
  return levelOne.getLevelTwo().getLevelThreeList().get(0).getLevelFourMap().get("key").getLevelFourName();
  return levelOne
          .getLevelTwo() // NullPointerException is thrown if levelOne is null, or so on...
          .getLevelThreeList()
          .get(0)
          .getLevelFourMap()
          .get("key")
          .getLevelFourName();
}
```

Unless it is certain that none of the objects will ever be null (which is rarely the case!), it wouldn't hurt to include exception handling or null checks.

With exception handling:

```java
public String getName(LevelOne levelOne) {
  try {
    return levelOne.getLevelTwo().getLevelThreeList().get(0).getLevelFourMap().get("key").getLevelFourName();
    return levelOne
            .getLevelTwo()
            .getLevelThreeList()
            .get(0)
            .getLevelFourMap()
            .get("key")
            .getLevelFourName();
  } catch (Exception e) {
    return null;
  }
```

## Concatenated Null Checks

In this method, we concatenate a list of null checks using `&&` condition. If the list of conditions is true, then it would be safe to get `levelFourName` using a chain of getters.

```java
public String getName(LevelOne levelOne) {
  if (
    levelOne != null
    && levelOne.getLevelTwo() != null
    && levelOne.getLevelTwo().getLevelThreeList() != null
    && !levelOne.getLevelTwo().getLevelThreeList().empty()
    && levelOne.getLevelTwo().getLevelThreeList().get(0).getLevelFourMap() != null
    && levelOne.getLevelTwo().getLevelThreeList().get(0).getLevelFourMap().contains("key")
    && levelOne.getLevelTwo().getLevelThreeList().get(0).getLevelFourMap().get("key") != null
  ) {
    return levelOne
            .getLevelTwo()
            .getLevelThreeList()
            .get(0)
            .getLevelFourMap()
            .get("key")
            .getLevelFourName();
  }
}
```

So far, we've only been able to retrieve a single field `levelFourName`. To retrieve multiple fields (e.g. `levelTwoName` and `levelFourName`), we will need to use multiple chain of getters.

```java
public List<String> getNames(LevelOne levelOne) {
  List<String> result = new ArrayList<>();
  if (
    levelOne != null
    && levelOne.getLevelTwo() != null
    && levelOne.getLevelTwo().getLevelThreeList() != null
    && !levelOne.getLevelTwo().getLevelThreeList().empty()
    && levelOne.getLevelTwo().getLevelThreeList().get(0).getLevelFourMap() != null
    && levelOne.getLevelTwo().getLevelThreeList().get(0).getLevelFourMap().contains("key")
    && levelOne.getLevelTwo().getLevelThreeList().get(0).getLevelFourMap().get("key") != null
  ) {
    // Add LevelTwoName to result
    result.add(levelOne
            .getLevelTwo()
            .getLevelTwoName();
    
    // Add LevelFourName to result
    result.add(levelOne
            .getLevelTwo()
            .getLevelThreeList()
            .get(0)
            .getLevelFourMap()
            .get("key")
            .getLevelFourName());
  }
  return result;
}
```

This method is inefficient considering that we are calling getters on same objects multiple times. Plus, we are unable to retrieve `levelTwoName` when  `levelFourMap` or `levelFour` is null. To handle this scenario, we will need to create two almost similar looking methods `getLevelTwoName()` and `getLevelFourName()`, which again will be calling repeated getters which is really inefficient.

## Optional

The [Optional](https://www.baeldung.com/java-optional) class was introduced in Java 8. While this method follows proper coding convention, it can be difficult to write and debug. I.e. when to use `map`, `filter`, `stream`, `get`, `orElse`, etc...? Plus, the behaviour and return type of each method is not immediately obvious.

```java
public getNames(LevelOne levelOne) {
  return Optional.ofNullable(levelOne)
          .map(LevelOne::getLevelTwo)
          .map(LevelTwo::getLevelThreeList)
          .filter(list -> !list.empty())
          .map(list -> list.get(0))
          .map(LevelThree::getLevelFourMap)
          .map(map -> map.get("key"))
          .map(LevelFour::getName)
          .orElse(null);
}
```

## StatementHandler

First, we will need to implement the `StatementHandler` and `StaticStatementHandler` classes. We can put them in a `util` package as a common utility class:

```java
package com.example.common.util;

/**
 * This class contains several closures for wrapping chained method calls. The closure can
 * execute either an optional call chain. If an optional call chain fails with an NPE, a null will be returned.
 */
@Component
public class StatementHandler {

  public <T> T optional(Supplier<T> statement) {
    return StaticStatementHandler.optional(statement);
  }

}

public final class StaticStatementHandler {

  public static <T> T optional(Supplier<T> statement) {
    try {
      return statement.get();
    } catch (Exception exc) {
      return null;
    }
  }
}
```

Then, we can make use of `StatementHandler.optional()` to parse our nested object:

```java
package com.example.levelone;

import com.example.common.util.StatementHandler;

public class LevelOneController {

  @Autowired
  StatementHandler statementHandler;

  public String getName(LevelOne levelOne) {
    return statementHandler.optional(() -> 
      levelOne
        .getLevelTwo()
        .getLevelThreeList()
        .get(0)
        .getLevelFourMap()
        .get("key")
        .getLevelFourName();
    );
  }

}
```

This method basically abstracts the `try and catch exception` block into the `StaticStatementHandler` class so that it is safe to use the chain of getters method.

## Nested Null Checks

This method __traverses__ the nested data structure level by level. This allows us to retrieve `levelTwoName` even if the remaining nested objects are null (e.g. if `levelFourMap` is null). However, this method has poor readability.

```java
public List<String> getNames(LevelOne levelOne) {
  List<String> result = new ArrayList<>();
  if (levelOne != null) {
    LevelTwo levelTwo = levelOne.getLevelTwo();
    if (levelTwo != null) {
      // Add levelTwoName to result
      result.add(levelTwo.getLevelTwoName());
      List<LevelThree> levelThreeList = levelTwo.getLevelThreeList();
      if (levelThreeList != null && !levelThreeList.empty()) {
        Map<String, LevelFour> levelFourMap = levelThreeList.get(0).getLevelFourMap();
        if (levelFourMap != null && levelFourMap.contains("key")) {
          LevelFour levelFour = levelFourMap.get("key");
          if (levelFour != null) {
            // Add levelFourName to result
            result.add(levelFour.getLevelFourName());
          }
        }
      }
    }
  }
  return result;
}
```

## Flattened Null Checks

We can flatten the traversal using the following two options.

Option 1: Skip assignment if null

```java
public List<String> getNames(LevelOne levelOne) {
  List<String> result = new ArrayList<>();

  LevelTwo levelTwo;
  if (levelOne != null) {
    levelTwo = levelOne.getLevelTwo();
  }

  List<LevelThree> levelThreeList;
  if (levelTwo != null) {
    // Add levelTwoName to result
    result.add(levelTwo.getLevelTwoName());
    levelThreeList = levelTwo.getLevelThreeList();
  }

  Map<String, LevelFour> levelFourMap;
  if (levelThreeList != null && !levelThreeList.empty()) {
    levelFourMap = levelThreeList.get(0).getLevelFourMap();
  }

  LevelFour levelFour;
  if (levelFourMap != null && levelFourMap.contains("key")) {
    levelFour = levelFourMap.get("key");
  }

  if (levelFour != null) {
    // Add levelFourName to result
    result.add(levelFour.getLevelFourName());
  }

  return result;
}
```

Option 2: Return __null__ immediately if null

```java
public List<String> getNames(LevelOne levelOne) {
  List<String> result = new ArrayList<>();

  if (levelOne == null) {
    return null;
  }

  LevelTwo levelTwo = levelOne.getLevelTwo();
  if (levelTwo == null) {
    return null;
  }

  // Add levelTwoName to result
  result.add(levelTwo.getLevelTwoName());

  List<LevelThree> levelThreeList = levelTwo.getLevelThreeList();
  if (levelThreeList == null || levelThreeList.empty()) {
    return null;
  }

  Map<String, LevelFour> levelFourMap = levelThreeList.get(0).getLevelFourMap();
  if (levelFourMap == null || !levelFourMap.contains("key")) {
    return null; 
  }
  
  LevelFour levelFour = levelFourMap.get("key");
  if (levelFour == null) {
    return null;
  }

  // Add levelFourName to result
  result.add(levelFour.getLevelFourName());

  return result;
}
```

Option 3: Return __result__ immediately if null

```java
public List<String> getNames(LevelOne levelOne) {
  List<String> result = new ArrayList<>();

  if (levelOne == null) {
    return result;
  }

  LevelTwo levelTwo = levelOne.getLevelTwo();
  if (levelTwo == null) {
    return result;
  }

  // Add levelTwoName to result
  result.add(levelTwo.getLevelTwoName());

  List<LevelThree> levelThreeList = levelTwo.getLevelThreeList();
  if (levelThreeList == null || levelThreeList.empty()) {
    return result;
  }

  Map<String, LevelFour> levelFourMap = levelThreeList.get(0).getLevelFourMap();
  if (levelFourMap == null || !levelFourMap.contains("key")) {
    return result; 
  }
  
  LevelFour levelFour = levelFourMap.get("key");
  if (levelFour == null) {
    return result;
  }

  // Add levelFourName to result
  result.add(levelFour.getLevelFourName());

  return result;
}
```

### Which Option Is Better?

__Option 2__ and __Option 3__ has better readability and is straighforward -- immediately return null or result once a `null` object is found.

However, __Option 1__ is better for two reasons:

1. It handles the case where `levelTwoName` exists, but `levelFourMap` or `levelFour` objects are null, which cannot be achieved using option 2.
1. It handles certain cases where `levelTwo` does not exist, but `levelFourName` exists, which cannot be achieved using option 3.
1. Fewer test cases need to be written to achieve 100% code coverage. Options 2 and 3 require __5__ unit tests and __4__ helper methods while option 1 requires only __1__ unit test and __1__ helper method.

__Unit tests for `option 1` (1 unit tests, 1 helper method, 100% code coverage):__

```java
@Test
public void getNamesTest_shouldReturnListWithTwoStrings() {
  LevelOne levelOne = LevelUtil.getLevelOne();
  List<String> result = getNames(levelOne));
  assertEquals(2, result.size());
  assertEquals("levelTwoName", result.get(0));
  assertEquals("levelFourName", result.get(1));
}
```

__Unit tests for `option 2` (5 unit tests, 4 helper methods, 100% code coverage):__

```java
@Test
public void getNamesTest_levelOneNull_shouldReturnNull {
  LevelOne levelOne = null;
  assertNull(getName(levelOne));
}

@Test
public void getNamesTest_levelTwoNull_shouldReturnNull {
  LevelOne levelOne = LevelUtil.getLevelOneWithLevelTwoNull();
  assertNull(getName(levelOne));
}

@Test
public void getNamesTest_levelThreeNull_shouldReturnListWithOneString {
  LevelOne levelOne = LevelUtil.getLevelOneWithLevelThreeListNull();
  List<String> result = getNames(levelOne));
  assertEquals(1, result.size());
  assertEquals("levelTwoName", result.get(0));
}

@Test
public void getNamesTest_levelFourNull_shouldReturnListWithOneString {
  LevelOne levelOne = LevelUtil.getLevelOneWithLevelFourMapNull();
  List<String> result = getNames(levelOne));
  assertEquals(1, result.size());
  assertEquals("levelTwoName", result.get(0));
}

@Test
public void getNamesTest_levelFourNull_shouldReturnListWithTwoStrings {
  LevelOne levelOne = LevelUtil.getLevelOne();
  List<String> result = getNames(levelOne));
  assertEquals(2, result.size());
  assertEquals("levelTwoName", result.get(0));
  assertEquals("levelFourName", result.get(1));
}
```

__LevelUtil:__

```java
public class LevelUtil {
  public static LevelOne getLevelOne() {
    // LevelOne
    LevelOne levelOne = new LevelOne();

    // LevelTwo
    LevelTwo levelTwo = new LevelTwo();
    levelTwo.setName("levelTwoName");
    levelOne.setLevelTwo(levelTwo);

    // LevelThree
    List<LevelThree> levelThreeList= new ArrayList<>();
    LevelThree levelThree = new LevelThree();
    levelThreeList.add(levelThree);
    levelTwo.setLevelThreeList(levelThreeList);

    // LevelFour
    Map<String, LevelFour> levelFourMap = new HashMap<>();
    LevelFour levelFour = new LevelFour();
    levelFour.setName("levelFourName");
    levelThree.setLevelFourMap(levelFourMap);

    return levelOne;
  }
  
  public static LevelOne getLevelOneWithLevelTwoNull() {
    LevelOne levelOne = getLevelOne();
    levelOne.setLevelTwo(null);
    return levelOne;
  }
  
  public static LevelOne getLevelOneWithLevelThreeListNull() {
    LevelOne levelOne = getLevelOne();
    levelOne.getLevelTwo().setLevelThreeList(null);
    return levelOne;
  }
  
  public static LevelOne getLevelOneWithLevelFourMapNull() {
    LevelOne levelOne = getLevelOne();
    levelOne.getLevelTwo().getLevelThreeList().get(0).setLevelFourMap(null);
    return levelOne;
  }

}

```
