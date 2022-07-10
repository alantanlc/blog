
# Kafka

## Overview

1. Key Concepts
1. Topic Creation 
1. Kafka Connection
1. Consumer
1. Producer
1. Profile Segregation
1. Replication 

## Key Concepts

1. Cluster
1. Topic
1. Partition and Offset  

### Cluster



Sample values:

```
NAU-1100
NAU-1101
NAP-1200
NAP-1201
```

### Topic

Topics are where your application produce messages to and consume messages from.

A typical naming convention for kafka topics can be like this:

```xml
<PRODUCER_SYSTEM>-<CONSUMER_SYSTEM>-<REQUEST>-<ENVIRONMENT>
```

A topic where `apigateway` is the __producer__ and `payment` is the __consumer__. Incoming payment __requests__ are sent over this topic in the __uat__ environment would look like this:

```
apigateway-payment-sg-request-uat
```

A topic where `payment` is the __producer__ and `apigateway` is the __consumer__, where payment __responses__ are sent over this topic in the __uat__ environment would look like this:
```
apigateway-payment-sg-response-uat
apigateway-payment-sg-request-prod
apigateway-payment-sg-response-prod
```

### Partition And Offset

TODO

## 

## Consumer Listener

TODO

## Producer

TODO

## Replication

1. The unit of replication is the topic partition. Under non-failure conditions, each partition has a single leader and zero or more followers.
1. Total number of replicas including the leader constitutes to the replication factor.
1. All writes go to the leader and reads can go to the leader or the followers of the partition.


### Kafka Node Liveness

Kafka node liveness has two conditions:

1. Node must be able to maintain its session with Zookeeper (via Zookeeper's heartbeat mechanism)
1. As a follower, it must replicate the writes happening on the leader and not fall too far behind

If a follower dies, gets stucks, or falls behind, the leader will remove the follower from the list of in sync replicas.

