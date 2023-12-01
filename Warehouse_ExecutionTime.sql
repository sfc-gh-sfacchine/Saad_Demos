USE WAREHOUSE DEMO_WH;

SELECT query_id,
  ROW_NUMBER() OVER(ORDER BY partitions_scanned DESC) AS query_id_int,
  query_text,
  total_elapsed_time/1000 AS query_execution_time_seconds,
  partitions_scanned,
  partitions_total
FROM snowflake.account_usage.query_history Q
ORDER BY total_elapsed_time desc
LIMIT 50;