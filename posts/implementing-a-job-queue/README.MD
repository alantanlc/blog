# Implementing A Job Queue

## The Job Data Model

Data Model:

1. ID
1. NAME
1. SHA
1. CREATED_DTTM
1. LAST_H_DTTM

## Picking up new jobs in a FIFO order

```sql
BEGIN TRANSACTION;

SELECT *
FROM JOB
WHERE STATUS = 'UNPROCESSED'
ORDER BY CREATED_DTTM
LIMIT 1;

ROLLBACK;

UPDATE JOB
SET STATUS = 'IN_PROGRESS'
WHERE ID = JOB_ID;

COMMIT;
```

1. Get the oldest unprocessed job from table
1. Update status to in progress
1. In the event if no job is available, the transaction should be rolled back
1. If update is successful, then commit the transaction changes to the database
 