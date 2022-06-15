
# Code Coverage With IntelliJ, Jacoco And SonarQube

A quick guide on how to check for code coverage using IntelliJ, Jacoco, and SonarQube.

## Overview

1. IntelliJ
1. Jacoco and SonarQube

## IntelliJ

1. Run configuration
1. Inclusions and exclusions
1. Results

### Run Configuration

You can select a package or class to run tests with coverage. A run configuration is automatically created which you can then modify as necessary.

### Inclusions and Exclusions

1. Open up the run configuration that has been created
1. Select the 'Code Coverage' tab
1. Specify the class or package to include and exclude accordingly

### Results

Run tests with coverage:

1. Open up IntelliJ File Explorer
1. Right click on desired class or package
1. Select `Run tests with coverage`

__Coverage console__

1. Once the run is completed, the Coverage console should appear on a right pane
1. This console shows the coverage percentages by methods and lines
1. You can navigate up and down the directory tree to get the coverage of each specific package and class

__File explorer__

1. On the file explorer, the class method and line coverage percentages are also displayed on each level of package and class.

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

Run `mvn clean package`

__Jacoco site report__

1. Navigate to `target/jacoco/site` folder
1. Open `index.html` with a web browser
1. Test coverage percentages are shown by package and class level
 
__SonarQube report__

1. Navigate to your hosted SonarQube site (e.g. localhost:9000)
 
