
# Deploying app using `cf push`

## Overview

1. Build the JAR
1. Update `manifest-local.yml`
1. cf api login
1. `cf push` your application

## Build the Jar

Update __artifactId__ and __version__ in `pom.xml`:

```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId> <!-- name -->
    <version>1.0.0-SNAPSHOT</version> <!-- version -->
</project>
```

Build your application:

```shell
$ mvn clean package
```

You should find the JAR file in the `target` folder.

```
my-app
    |_ manifest
    |_ src
    |_ target
        |_ my-app-1.0.0-SNAPSHOT.jar
    |_ pom.xml
```

## Update `manifest-local-yml`

The `manifest-local.yaml` is usually placed in the `manifest` folder.

```
my-app
    |_ manifest
        |_ manifest-jules.yml
        |_ manifest-local.yml
    |_ src
    |_ target
    |_ pom.xml
```

Update the `path` value to the location of your JAR file.

```yml
---
applications:
- name: my-app
    path: ../target/my-app.1.0.0-SNAPSHOT.jar
    instances: 1
    memory: 2G
    buildpacks:
    - java_buildpack
```

## cf api login

Update your cf api and login:

```shell
$ cf login -a https://api.example.com -u username
API endpoint: https://api.example.com

Password>
Authenticating...
OK

Targeted org example-org

Targeted space development




API endpoint:   https://api.example.com
User:           username
Org:            example-org
Space:          development
```

## `cf push` your application

Run this command in the `manifest` folder:

```shell
$ cf push my-app -f manifest-local.yml
Creating app my-app in org example-org / space development as user...
OK

Creating route my-app.example.com...
OK
...

1 of 1 instances running

App started
...

request state: started
instances: 1/1
usage: 2G x 1 instances
urls: my-app.example.com
last uploaded: Wed Jun 8 23:43:15 UTC 2022
stack: cflinuxfs3
buildpack: java_buildpack

    state       since                       cpu     memory      disk        details
#0  running     2022-06-08 04:44:07 PM      0.0%    0 of 2G     0 of 2G
```
