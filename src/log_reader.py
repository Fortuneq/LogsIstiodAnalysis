import requests
import json
import time


class LogReader:
    def __init__(self, loki_url, query):
        self.loki_url = loki_url
        self.query = query

    @staticmethod
    def get_unix_epoch_time_in_ns(minutes_ago):
        return int((time.time() - (minutes_ago * 60)) * 1e9)

    def get_logs_from_loki(self, start_time, end_time, limit=1000):
        params = {
            "query": self.query,
            "limit": limit,
            "start": start_time,
            "end": end_time,
        }
        response = requests.get(self.loki_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching logs: {response.status_code} - {response.text}")
            return None

    def fetch_logs_last_5_minutes(self):
        end_time = self.get_unix_epoch_time_in_ns(0)  # Current time
        start_time = self.get_unix_epoch_time_in_ns(1)  # 5 minutes ago
        return self.get_logs_from_loki(start_time, end_time)

    def get_logs(self):
        log_stream = []
        logs = self.fetch_logs_last_5_minutes()
        # print("RAW_LOGS: ")
        # print(logs)
        if logs:
            for stream in logs["data"]["result"]:
                for values in stream["values"]:
                    log_stream.append(values[1] + "\n")
        return log_stream
