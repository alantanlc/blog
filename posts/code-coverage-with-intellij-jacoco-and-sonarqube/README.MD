
# Code Coverage With IntelliJ, Jacoco And SonarQube

A quick guide on how to check for code coverage using IntelliJ, Jacoco, and SonarQube.

## Overview

1. IntelliJ
1. Jacoco and SonarQube

## IntelliJ

1. Run configurations
1. Test exclusions
1. Results

### Run Configurations

TODO

### Test Exclusions

1. `**`: Zero or more directories
1. `*`: Zero or more characters
1. `?`: TODO

```xml
<!-- pom.xml -->
<plugins>
    <plugin>
        <configuration>
            <excludes>
                <exclude>**/com/tech/payment/config/**/*</exclude>
                <exclude>**/com/tech/payment/constants/*Enum.class</exclude>
                <exclude>**/com/tech/payment/kafka/**/*</exclude>
            </excludes>
        </configuration>
    </plugin>
</plugins>
```

### Results

Run tests with coverage:

1. Open up IntelliJ File Explorer
1. Right click on root package
1. Select `Run tests with coverage`

Converage console:

1. Once all tests are run, the Coverage console should appear on the right
1. Console shows the coverage by methods and lines in terms of percentages
1. You can navigate up and down the directory tree to see the coverage of each package and class

File explorer:

1. On file explorer, the class method and line coverage percentages are also displayed on each level of package and class

## Jacoco and SonarQube

1. Maven configuration
1. Test exclusions
1. Results

### Maven Configuration

TODO

### Test Exclusions

TODO

### Results 

1. Jacoco site report
1. SonarQube report
