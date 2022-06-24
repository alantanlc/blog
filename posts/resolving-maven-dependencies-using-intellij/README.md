
# Resolving Maven Dependencies Using IntelliJ

## Overview

1. Set up Maven project in IntelliJ
1. Basic knowledge of Maven
1. The Maven tab in IntelliJ 
1. Update dependencies of your maven project

## Set Up Maven Project in IntelliJ

1. Navigate to `File` > `Project Structure` > `Modules`
1. Click on `+` > `Import Exisiting Project`

## Basic Knowledge Of Maven

Minimally, you should know that a dependency has the following defined:

1. Group
1. Artifact
1. Version

## The Maven Tab In IntelliJ

Two ways to open up the Maven tab:

1. By default, the Maven tab is collapsed on the right side of IntelliJ. Simply click and the Maven tab will open up
1. Use CTRL+SHIFT+A and search for `Maven`

On the Maven tab, you will see a list of Maven projects that are imported into IntelliJ. When you expand a project, you will see:

1. Lifecycle
1. Dependencies

### Lifecyle

1. clean
1. compile
1. test
1. package
1. verify
1. install
1. site 
1. deploy

### Dependencies

This expands as a tree to all the dependencies of the Maven project.

Each entry shows the group, artifact, and version that is eventually resolved and imported for the project based on `pom.xml`.

## Update Dependencies Of Your Maven Project

The following are the typical steps to execute:

1. Make changes in `pom.xml` (Remember to save the file!)
1. Reimport dependencies
1. Verify that libraries and versions are updated properly
1. Resolve errors in source code 
1. Run application
