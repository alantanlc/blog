
# Liquibase

## Topics

1. Never modify a changeSet that has already been executed
1. Resolving checksum errors
1. Resolving liquibase errors during local development
1. Primary key contraint violation
1. Using `onFail="markRan"` and `onError="markRan"`
1. Use sequences over max

## Never modify a change set that has already been executed

When a liquibase changeset is successfully executed, a new entry is created in the `DATABASECHANGELOG` table.

```xml
<changeSet id="payment_alan_3" author="alan">
  <insert tableName="payment">
    <column name="id" valueSequence="payment_seq">
    <column name="legal_entity" value="123" />
    <column name="clearing_system" value="sgFast" />
  </insert>
</changeSet>
```

Check the `DATABASECHANGLOG` table:

```sql
SELECT * FROM DATABASECHANGELOG ORDER BY DATE EXECUTED DESC;
```

__DATABASECHANGELOG__ table:

| ID | AUTHOR | FILENAME | DATEEXECUTED | ORDEREXECUTED | EXECTYPE | MD5SUM |
| - | - | - | - | - | - | - |
| payment_alan_3 | alan | payment.xml | 20220622 | 3 | EXECUTED | 02558a70324e7c4f269c69825450cec8 |
| payment_alan_2 | alan | payment.xml | 20220622 | 2 | EXECUTED | 73df9317ef7c5bc5d038760213d7336c |
| payment_alan_1 | alan | payment.xml | 20220622 | 1 | EXECUTED | 0fd078e5d26aa14cd6a9594eb6ec08cd |

If you were to modify `payment_alan_3` and run your application, liquibase would throw an error and your application will fail to start:

```xml
<changeSet id="payment_alan_3" author="alan">
  <insert tableName="payment">
    <column name="id" valueSequence="PAYMENT_SEQ">
    <column name="legal_entity" value="123" />
    <column name="clearing_system" value="auNpp" /> <!-- modified -->
  </insert>
</changeSet>
```

Error log

```

```
Note: Refer to `Resolving checksum errors` when this happens.

Such errors can be easily prevented. A general guideline is to __never modify any changeset that has already been pushed to a shared repository__.

This is because any application that picks up this modification and has already executed the previous version of this changeset will fail to start. It could be a developer working on local environment, or worse, the production environment! Either way, someone will certainly be hunting you down for causing this problem.

__What You Should Do Instead__

Create a new changeset to modify the previous changeset. Since in `payment_alan_3` we have inserted an entry with `clearing_system` as `sgFast` and now we want to change the value to `auNpp`, we perform an update using a new changeset:

```xml
<changeSet id="payment_alan_4" author="alan">
  <update tableName="payment">
    <column name="clearing_system" value="auNpp" />
    <where>clearing_system = "sgFast"</where>
  </update>
</changeSet>
```

## Resolving Checksum Errors

It is occasionally inevitable that checksum error-causing code gets merged and deployed. When this happens, there are generally a few ways to resolve the problem:

1. Revert the modification in code
1. Manually update the checksum value in `DATABASECHANGELOG` table
1. Delete the changeset from `DATABASECHANGELOG` table

### Revert the modification in code

This should be the default approach for most occasions because it is a change in a single place (the source code) and the fix can be applied all environments by deployment (e.g. having DEV, UAT, PROD environments, and the modification was deployed to all these environments).

The downside of this approach is that it requires a new build and deployment of application artifacts to the environment. In certain scenarios, e.g during a tight deployment window in PROD, this approach may not be feasible.

### Manually update the checksum value in `DATABASECHANGELOG` table

When your application fails to start due to a liquibase error, you will find a log like this, typically within the last 20 lines of your log file:

```

```

The error log contains the new checksum of the modified changeset. You can manually update the checksum value in database and restart your application.

```sql
UPDATE DATABASECHANGELOG SET CHECKSUM = '657f8b8da628ef83cf69101b6817150a' WHERE ID = 'payment_alan_3';
```

### Delete the changeset from `DATABASECHANGELOG` table

By deleting the entry from database and restarting your application, the modified changeset will be executed again.

```sql
DELETE FROM DATABASECHANGELOG WHERE ID = `payment_alan_3`;
```

## Resolving Liquibase Errors During Local Development

Someone has checked in some liquibase error-causing changeset and you unfortunately pulled it to your local repository.

Don't read too much into the issue! More often than not, they are careless mistakes that should be resolved by the originating author.

Instead, simply comment out the changeset or even the entire changelog file if you don't need the liquibase changes for your local development and re-run your application.

```xml
<!--
<changeSet id=“payment_alan_3” author=“alan”>
  <insert tableName=“payment”>
    <column name=“id” valueSequence=“PAYMENT_SEQ”>
    <column name=legal_entity” value=“123” />
    <column name=“clearing_system” value=“auNpp” /> <!— modified —>
  </insert>
</changeSet>
-->
```

Be sure not to check in the temporary comment!

## Primary Key Constraint Violation

TODO

## Using `onFail="markRan"` and `onError="markRan"`

TODO

## Using Sequences Over Max

TODO
