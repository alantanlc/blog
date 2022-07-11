# Config Service

## Overview

1. Service without config service
1. Service with config service
1. Pros and Cons
1. References

## Service without config service

The configuration files (e.g. `application.yaml`, `application.properties`, `bootstrap.yaml`) will be maintained in the `resources` directory of your service application.

```
my-app
|_ src
    |_ main
        |_ java
        |_ resources
            |_ application.yaml
            |_ application-local.yaml
            |_ application-dev.yaml
            |_ application-uat.yaml
            |_ application-prod.yaml
|_ test
|_ pom.xml
```

application.yaml:

```yaml
spring:
    application:
        name: my-app

server:
    port: 8080
```

application-dev.yaml:

```yaml
server:
    port: 8081
```

application-uat.yaml:

```yaml
server:
    port: 8082
```

application-prod.yaml:

```yaml
server:
    port: 8083
```

Running the application with profiles:

```shell
$ mvn spring-boot:run -Dpring.profiles.active=dev
```

## Service with config service

Using a config service, we will place our configuration properties in environment specific directories (e.g. dev, uat, prod, local). Notice that the file name is now renamed to the actual application name (i.e. `dev/my-app.yaml` instead of previously `resource/application-dev.yaml`):

```
config-service
|_ src
    |_ main
        |_ java
            |_ demo
                |_ ConfigServerApplication.yaml
        |_ resources
            |_ application.yaml
            |_ dev
                |_ my-app.yaml
            |_ uat
                |_ my-app.yaml
            |_ prod
                |_ my-app.yaml
            |_ local
                |_ my-app.yaml
|_ test
|_ pom.xml
```

application.yaml

```yaml
spring:
    application:
        name: configserver

server:
    port: 8888
```

Add the `@EnableConfigServer` annotation in your main application class:

```java
package demo;

import org.springframework.cloud.config.server.EnableConfigServer;

@EnableConfigServer
public class ConfigServerApplication {

    public static void main(String args[]) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}
```

Run the config service app:

```shell
$ mvn spring-boot:run
```

You can then retrieve the configuration by __app__ and __profile__ using the config service endpoint:

```
http://localhost:8888/{app}/{profile}
```

Example:

```
http://localhost:8888/my-app/local
http://localhost:8888/my-app/dev
http://localhost:8888/my-app/uat
http://localhost:8888/my-app/prod
```

Then in our `my-app` application, we simply specify the spring cloud config uri in `resources/application.yaml`:

```
my-app
|_ src
    |_ main
        |_ java
        |_ resources
            |_ application.yaml
|_ test
|_ pom.xml
```

```yaml
spring:
    cloud:
        config:
            uri: ${CONFIG_SERVER_URI:${vcap.services.${PREFIX:}configserver.credentials.uri:http://user:password@localhost:8888}}
```

Running the application is the same, we simply specify the active profiles to use:

```shell
$ mvn spring-boot:run -Dpring.profiles.active=dev
```

## Pros and Cons

Pros of using a config service:

1. Configuration properties are maintained in a common repository
1. No need to build and deploy service application due to config change. Make changes in config service repository and redeploy config service
1. Build, deploy and app start up time of a config service is usually much faster than a service application

## References

https://spring.io/projects/spring-cloud-config#overview
