# Parsing Nested Data Structure

## Overview

1. Nested Data Structure
1. The bad way
1. Nested null checks
1. Unnested null checks
1. Optional
1. StatementHandler
1. Mapstruct 

## Nested Data Structure

```java
class LevelOne {
  LevelTwo levelTwo;
}

class LevelTwo {
  LevelThree levelThree;
}

class LevelThree {
 LevelFour levelFour:
}
``` 

## The Bad Way

```java
public void getName(LevelOne levelOne) {
String name = levelOne.getLevelTwo
```   