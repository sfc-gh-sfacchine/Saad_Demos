USE WAREHOUSE DEMO_WH;

SELECT query_id,
  ROW_NUMBER() OVER(ORDER BY partitions_scanned DESC) AS query_id_int,
  query_text,
  total_elapsed_time/1000 AS query_execution_time_seconds,
  partitions_scanned,
  partitions_total
FROM snowflake.account_usage.query_history Q
WHERE warehouse_name = 'my_warehouse' AND TO_DATE(Q.start_time) > DATEADD(day,-1,TO_DATE(CURRENT_TIMESTAMP()))
  AND total_elapsed_time > 0 --only get queries that actually used compute
  AND error_code IS NULL
  AND partitions_scanned IS NOT NULL
ORDER BY total_elapsed_time desc
LIMIT 50;