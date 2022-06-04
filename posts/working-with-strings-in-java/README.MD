
# Working With Strings In Java

## Overview

1. StringUtils

## StringUtils

1. Difference between `isNotEmpty()` and `isNotBlank()`
1. When to use `StringUtils.equals(s1, s2)` and `s1.equals(s2)`

### Difference between `isNotEmpty()` and `isNotBlank()`

__isNotEmpty()__

```java
StringUtils.isNotEmpty(null)    // false
StringUtils.isNotEmpty("")      // false
StringUtils.isNotEmpty(" ")     // true
StringUtils.isNotEmpty("hi")    // true
StringUtils.isNotEmpty(" hi ")  // true
```

__isNotBlank__

```java
StringUtils.isNotBlank(null)    // false
StringUtils.isNotBlank("")      // false
StringUtils.isNotBlank(" ")     // false
StringUtils.isNotBlank("hi")    // true
StringUtils.isNotBlank(" hi ")  // true
```

The only difference between `isNotEmpty` and `isNotBlank` is that the former returns true while the latter returns false when the given string contains only whitespaces (e.g. " ").

Arguably, in most cases, we are usually expecting the string of interest to contain some non-whitespace characters (e.g. "hi").

As such, prefer to use `isNotBlank` over `isNotEmpty` by default unless otherwise specified. Likewise, prefer to use `isBlank` over `isEmpty`.

### When to use `StringUtils.equals(s1, s2)` and `s1.equals(s2)`

`StringUtils.equals(s1, s2)` provides a null-safe comparison unlike `s1.equals(s2)`.

Consider the scenario below, which option is better?

```java
String s1 = null;
String s2 = "hi";
boolean flag = False;

if (StringUtils.(s1, s2)) {     // false
    flag = true;
}

if (s1.equals(s2)) {            // throws NullPointerException
    flag = true;
}
```

It depends on the significance of `flag` (or whatever code that falls within the `if` block).

Perhaps you are writing a non-critical application where `flag` is eventually just a value displayed on the web page. The null-safe option would not cause  a break in the program flow (at least within your module/component/application) during runtime and you can always make the fix at a later time.

But what if you are writing a software for a space rocket launch and not updating `flag` may potentially fail to activate another module at a critical moment? In this case, you might want to use the latter option so that such errorneous are caught and fixed up front before the software goes live.
