with raw as
(
select
           query_text,
           session_id,
           start_time,
           warehouse_name,
           user_name,
           query_id,
           execution_time,
    BYTES_SPILLED_TO_LOCAL_STORAGE,    -- Local spill
    BYTES_SPILLED_TO_REMOTE_STORAGE,  -- Remote spill
    queued_overload_time+queued_provisioning_time+queued_repair_time as queue_time,
    case when execution_time < 1000 then '0: 0 ~ 1 sec'
        when execution_time >= 1000 and execution_time < 10000 then '1: 1~10 Sec'
        when execution_time >= 10000 and execution_time <= 60000 then '2: 10 ~ 60 Sec'
        when execution_time > 60000 and execution_time <= 3600000 then '3: 1 min ~ 1 hour'
        when execution_time > 3600000 then '4: over an 1 hour'
        end as bucket,
    count(*) over (partition by warehouse_name) as total_count,
    TOTAL_ELAPSED_TIME
 from snowflake.account_usage.query_history j
 where j.start_time = :daterange
 --and latest_cluster_number is not null
)
select warehouse_name, bucket
, any_value(total_count) as WH_query_count
, count(*) as user_WH_query_count
, user_WH_query_count * 100 / WH_query_count as percentage
, avg(TOTAL_ELAPSED_TIME) /1000as avg_total_runtime_secs
, avg(execution_time) /1000 as avg_WH_secs
, max(TOTAL_ELAPSED_TIME) /1000as max_total_runtime_secs
, max(execution_time) /1000 as max_WH_secs
, avg(queue_time) /1000 as avg_queue_time
, max(queue_time) /1000 as max_queue_time
, avg(BYTES_SPILLED_TO_REMOTE_STORAGE) / power(1024, 2) as avg_mb_spill_remote
, avg(BYTES_SPILLED_TO_LOCAL_STORAGE) / power(1024, 2) as avg_mb_spill_local
, any_value(query_id) as example_query_id
from raw
group by 1, 2
order by 1, 2
;