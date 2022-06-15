
# Code Coverage With IntelliJ, Jacoco And SonarQube

A quick guide on how to check for code coverage using IntelliJ, Jacoco, and SonarQube.

## Overview

1. IntelliJ
1. Jacoco and SonarQube

## IntelliJ

1. Run configurations
1. Test exclusions
1. Results

### Run Configuration

You can select a package or class to run test with coverage. A run configuration is automatically created which you can modify as necessary.

### Inclusions and Exclusions

1. Open up the run configuration that has been created
1. Click on the 'Code Coverage' tab
1. You can specify the class or package to include and exclude in the 2 panes accordingly

### Results

Run tests with coverage:

1. Open up IntelliJ File Explorer
1. Right click on root package
1. Select `Run tests with coverage`

__Coverage console__

1. Once all tests are run, the Coverage console should appear on the right side
1. Console shows in terms of percentages the coverage by methods and lines
1. You can navigate up and down the directory tree to get the coverage of each specific package and class

__File explorer__

1. On file explorer, the class method and line coverage percentages are also displayed on each level of package and class.

## Jacoco and SonarQube

1. Maven configuration
1. Inclusions and exclusions
1. Results

### Maven Configuration

Add the following dependency in `pom.xml`:

```xml
<dependency>
    <groupId>org.jacoco</groupId> 
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.6</version>
</dependency>
```

### Inclusions and Exclusions

Wildcard syntax:

1. `**` matches zero or more directories
1. `*` matches zero or more characters
1. `?` matches a single character

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    
    <configuration>
        <includes>
            <include>**/com/tech/payment/**/*</include>
        </includes>
        <excludes>
            <exclude>**/com/tech/payment/config/**/*</exclude>
            <exclude>**/com/tech/payment/constants/*Enum.class</exclude>
            <exclude>**/com/tech/payment/kafka/**/*</exclude>
        </excludes>
    </configuration>
</plugin>
```

Here, we are:
1. Including any file in any sub-package under the sub-package `com.tech.payment`
1. Excluding any file in any sub-package under the sub-package `com.tech.payment.config`
1. Excluding any file ending with `Enum.class` in any sub-package under the sub-package `com.tech.payment.constants`
1. Excluding any file in any sub-package under the sub-package `com.tech.payment.kafka`

### Results 

1. Jacoco site report
1. SonarQube report
