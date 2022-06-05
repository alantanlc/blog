# Implementing A Job Queue

1. Job data model
1. Picking up jobs in FIFO order
1. Handling worker failures

## Job Data Model

Data Model:

1. ID
1. NAME
1. SHA
1. STATUS 
1. CREATED_DTTM
1. LAST_H_DTTM  
 
## Picking Up Jobs In FIFO Order

A worker picks up a new job from database by executing a transactional SQL:

1. Get the oldest UNPROCESSED job
1. Update status to IN_PROGRESS
1. In the event if no job is available, the transaction should be rolled back
1. If the status update is successful, then commit the transaction changes to the database and execute the task

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

## Handling Worker Failures

1. A worker that is in progress of executing a job should periodically update the timestamp of LAST_H_DTTM of the job entry (e.g every 3-5 minutes)
1. Another server periodically updates the status of IN_PROGRESS jobs to UNPROCESSED where the LAST_H_DTTM + HEARTBEAT_INTERVAL is lesser than CURRENT_TIMESTAMP

```sql
UPDATE JOB
SET STATUS = 'UNPROCESSED'
WHERE LAST_H_DTTM + HEARTBEAT_INTERVAL > CURRENT_TIMESTAMP
``` 