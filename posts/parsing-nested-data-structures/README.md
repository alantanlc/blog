# Parsing Nested Data Structure

## Overview

1. Nested Data Structure
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
  LevelTwo levelTwo;
}

class LevelTwo {
  List<LevelThree> levelThreeList;
}

class LevelThree {
 Map<String, LevelFour> levelFourMap:
}

class LevelFour {
  String name;
}
``` 

## The Bad Way

This is an extremely bad way of getting `name` because __NullPointerException__ is thrown when one of the objects is null unless it is certain that none of the objects will ever be null which is rarely the case. Plus, it wouldn't hurt to add null checks to be safe.

```java
public String getName(LevelOne levelOne) {
  return levelOne
          .getLevelTwo()
          .getLevelThreeList()
          .get(0)
          .getLevelFourMap()
          .get("key")
          .getName();
}
```

## Concatenated Null Checks

```java
public String getName(LevelOne levelOne) {
  if (
    levelOne != null
    && levelOne.getLevelTwo() != null
    && levelOne.getLevelTwo().getLevelThreeList() != null
    && !levelOne.getLevelTwo().getLevelThreeList().empty()
    && levelOne.getLevelTwo().getLevelThreeList().get(0).getLevelFourMap() != null
    && levelOne.getLevelTwo().getLevelThreeList().get(0).getLevelFourMap().contains("key")
  ) {
    return levelOne
            .getLevelTwo()
            .getLevelThreeList()
            .get(0)
            .getLevelFourMap()
            .get("key")
            .getName();
  }
}
```

## Nested Null Checks

```java
public String getName(LevelOne levelOne) {
  String name = null;
  if (levelOne != null) {
    LevelTwo levelTwo = levelOne.getLevelTwo();
    if (levelTwo != null) {
      List<LevelThree> levelThreeList = levelTwo.getLevelThreeList();
      if (levelThreeList != null && !levelThreeList.empty()) {
        Map<String, LevelFour> levelFourMap = levelThreeList.get(0);
        if (levelFourMap != null && levelFourMap.contains("key")) {
          LevelFour levelFour = levelFourMap.get("key");
          if (levelFour != null) {
            name = levelFour.getName();
          }
        }
      }
    }
  }
  return name;
}
```

## Flattened Null Checks

Option 1: Skip assignment if null

```java
public String getName(LevelOne levelOne) {
  LevelTwo levelTwo;
  if (levelOne != null) {
    levelTwo = levelOne.getLevelTwo();
  }

  List<LevelThree> levelThreeList;
  if (levelTwo != null) {
    levelThree = levelTwo.getLevelThreeList();
  }

  Map<String, LevelFour> levelFourMap;
  if (levelThreeList != null && !levelThreeList.empty()) {
    LevelThree levelThree = levelThreeList.get(0).getLevelFourMap();
  }

  LevelFour levelFour;
  if (levelFourMap != null && levelFourMap.contains("key")) {
    levelFour = levelFourMap.get("key");
  }

  String name = null;
  if (levelFour != null) {
    name = levelFour.getName();
  }

  return name;
}
```

Option 2: Return immediately if null

```java
public String getName(LevelOne levelOne) {
  if (levelOne == null) {
    return null;
  }

  LevelTwo levelTwo = levelOne.getLevelTwo();
  if (levelTwo == null) {
    return null;
  }

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

  return levelFourMap.getName();
}
```
