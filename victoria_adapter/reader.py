import requests
import json
import time


def get_logs_from_loki(loki_url, query, start_time, end_time, limit=1000):
    params = {"query": query, "limit": limit, "start": start_time, "end": end_time}
    response = requests.get(loki_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка при запросе логов: {response.status_code} - {response.text}")
        return None


def get_unix_epoch_time_in_ns(minutes_ago):
    return int((time.time() - (minutes_ago * 60)) * 1e9)


loki_url = "http://localhost:3100/loki/api/v1/query_range"
query = '{job="your_job_name"}'

# Временные рамки: последние 5 минут
end_time = get_unix_epoch_time_in_ns(0)
start_time = get_unix_epoch_time_in_ns(5)

# Получение логов
logs = get_logs_from_loki(loki_url, query, start_time, end_time)
log_stream = ""
if logs:
    for stream in logs["data"]["result"]:
        for values in stream["values"]:
            log_stream += values[1]
print(log_stream)
