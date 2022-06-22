
# Liquibase

## Topics

1. Use sequences over max
1. Never modify a changeSet that has already been executed
1. Manually fixing checksum errors in database
1. Understanding databasechangelog
1. Quick ways to resolve liquibase errors during local development
1. Using `onFail="markRan"` and `onError="markRan"`

# Never modify a change set that has already been executed

When a liquibase changeset is successfully executed, a new entry is created in the `DATABASECHANGELOG` table.

```xml
<changeSet id="payment_alan_3" author="alan">
  <insert tableName="PAYMENT">
    <column name="ID" valueSequence="PAYMENT.NEXTVAL">
    <column name="CLEARING_SYSTEM" value="SG_FAST" />
  </insert>
</changeSet>
```

Check the `DATABASECHANGLOG` table:

```sql
SELECT * FROM DATABASECHANGELOG ORDER BY DATE EXECUTED DESC;
```

__DATABASECHANGELOG__ table:

| ID | AUTHOR | FILENAME | DATEEXECUTED | ORDEREXECUTED | EXECTYPE | MD5SUM |
| - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| payment_alan_3 | alan | payment.xml | DATEEXECUTED | 3 | EXECUTED | 02558a70324e7c4f269c69825450cec8 |
| payment_alan_2 | alan | payment.xml | DATEEXECUTED | 2 | EXECUTED | 73df9317ef7c5bc5d038760213d7336c |
| payment_alan_1 | alan | payment.xml | DATEEXECUTED | 1 | EXECUTED | 0fd078e5d26aa14cd6a9594eb6ec08cd |

If you were to modify `payment_alan_3` and run your application, liquibase would throw an error and your application will fail to start:

```xml
<changeSet id=“payment_alan_3” author=“alan”>
  <insert tableName=“PAYMENT”>
    <column name=“ID” valueSequence=“PAYMENT.NEXTVAL”>
    <column name=“CLEARING_SYSTEM” value=“AU_NPP” /> <!-- modified -->
  </insert>
</changeSet>
```

Error log:

```

```