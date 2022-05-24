
# Scalable classes using Spring `@Components` and `@Autowired`

In this article, we will show you how to write a scalable abstract class using Spring `@Components` and `@Autowired`.

## Overview

1. Abstract Payment Processor
1. Country-specific Payment Processors
1. Use hashmap to store and retrieve country-specific payment processors
1. Payment RestController

## Abstract Payment Processor

```java
@Component
public abstract class PaymentProcessor {
    
    public Payment process(PaymentMessage message) {
        Payment payment = new Payment();
        payment.setCurrency(message.getCurrency());
        payment.setAmount(message.getAmount());
        payment.setUsdAmount(getUsdAmount(message.getAmount()));
        return payment;
    }

    public abstract BigDecimal getUsdAmount(BigDecimal amount);

}
```

## Country-specific Payment Processors

```java
/* SgpPaymentProcessor.java */
@Component("sgpPaymentProcessor")
public class SgpPaymentProcessor extends PaymentProcessor {

    private static final BigDecimal USD_CONVERSION_RATE = '1.4';
    
    @Override
    public BigDecimal getUsdAmount(BigDecimal amount) {
        return amount * USD_CONVERSION_RATE;
    }
}

/* MyPaymentProcessor.java */
@Component("myPaymentProcessor")
public class MyPaymentProcessor extends PaymentProcessor {

    private static final BigDecimal USD_CONVERSION_RATE = '4.39';
    
    @Override
    public BigDecimal getUsdAmount(BigDecimal amount) {
        return amount * USD_CONVERSION_RATE;
    }
}
```

## Use hashmap to store and retrieve country-specific payment processors

```java
/* ProcessPaymentAction.java */
@Component
public class ProcessPaymentAction {

    private static final String PAYMENT_PROCESSOR = 'PaymentProcessor';

    @Autowired
    HashMap<String, PaymentProcessor> paymentProcessorMap;

    @Autowired
    PaymentServiceImpl paymentService;

    public boolean execute(PaymentMessage paymentMessage) {
        // Get country-specific payment processor from hashmap
        String country = paymentMessage.getCountry().toLowerCase();
        PaymentProcessor paymentProcessor = paymentProcessorMap.get(country + PAYMENT_PROCESSOR);

        // Process payment
        Payment payment = paymentProcessor.process(paymentMessage);

        // Save payment
        paymentService.save(payment);
        
        // Return
        return true;
    }

}
```

## Payment RestController
```java
@RestController
public class PaymentController {

    @Autowired
    ProcessPaymentAction processPaymentAction;

    @PostMapping("/payment")
    boolean postPayment(@RequestBody PaymentMessage paymentMessage) {
        log.info("Request to initiate payment: {}", paymentMessage);
        boolean result = processPaymentAction.execute(paymentMessage);
        return result;
    }

}
```
