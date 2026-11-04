from manager import LogProcessingManager

# TO-DO create the components separately manager'a
# Composition -> aggregation

loki_url = "http://localhost:3100/loki/api/v1/query_range"
query = '{job="your_job_name"}'
log_file_path = "resources/logs.csv"

manager = LogProcessingManager(
    loki_url=loki_url,
    log_query=query,
    log_library_path=log_file_path,
    interval=5,
)
manager.start()
