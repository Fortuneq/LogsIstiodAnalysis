import threading
import sqlite3
import time
from datetime import datetime

from analyzer import LogAnalyzer
from logparser import IstioLogParser
from features import binary_features, numerical_features
from error_server import ErrorMetricsServer
from log_reader import LogReader  # Can be replaced with any DB


class LogProcessingManager:
    def __init__(self, loki_url, log_query, log_library_path, interval):
        print("LogReader created!")
        self.log_reader = LogReader(loki_url, log_query)
        print("LogAnalyzer created!")
        self.log_analyzer = LogAnalyzer(
            log_library_path=log_library_path,
            log_parser=IstioLogParser(binary_features, numerical_features),
        )
        print("ErrorMetricsServer created!")
        self.error_metrics_server = ErrorMetricsServer(
            8000, "my_metric", "Custom metric example"
        )
        self.interval = interval
        self.timer = None
        self.last_timestamp = datetime.min
        self.log_stream = []

    def start(self):
        self.timer = threading.Timer(self.interval, self.process_new_logs)
        self.timer.start()

    def process_new_logs(self):
        print("CHECKING...")
        logs = self.log_reader.get_logs()
        self.log_stream.extend(logs)
        # Process new data
        sim = self.log_analyzer.check_issue(self.log_stream)
        self.error_metrics_server.update_metric(sim)

        # Restart the timer
        self.timer = threading.Timer(self.interval, self.process_new_logs)
        self.timer.start()
        print("END OF CHECKING...")

    def stop(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
