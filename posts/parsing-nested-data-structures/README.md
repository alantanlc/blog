# Parsing Nested Data Structures

## Overview

1. Nested data structure
1. The bad way
1. Concatenated null checks
1. Nested null checks
1. Flattened null checks
1. Optional
1. StatementHandler
1. Mapstruct 

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

## The Bad Way

While `levelFourName` can be retrieved using a string of getters, this is an extremely bad way because __NullPointerException__ is thrown when one of the objects is null.

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

Unless it is certain that none of the objects will ever be null (which is rarely the case), it wouldn't hurt to include exception handling or null checks.

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

In this method, we concatenate a list of null checks using `&&` condition. If the list of conditions is true, then it would be safe to get `levelFourName` using a string of getters.

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

So far, we've been only able to retrieve a single field `levelFourName`. To retrieve multiple fields (e.g. `levelTwoName` and `levelFourName`), we will need use string of getters multiple times.

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

This method is inefficient considering that we are calling getters on same objects multiple times. Plus, this exmaple below is unable to retrieve `levelTwoName` when `levelFourMap` or `levelFour` is null. To handle this scenario, we will need to create two almost similar methods `getLevelTwoName()` and `getLevelFourName()`.

## Optional

TODO

## Nested Null Checks

The following methods traverses the nested data structure level by level. This allows us to retrieve `levelTwoName` even if the remaining nested objects are null (e.g. `levelFourMap` is null):

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

Needless to say, this method has poor readability.

## Flattened Null Checks

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

Option 2: Return immediately if null

```java
public List<String> getName(LevelOne levelOne) {
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
