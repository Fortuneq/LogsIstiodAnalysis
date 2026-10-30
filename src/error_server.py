from prometheus_client import start_http_server, Gauge
import time


class ErrorMetricsServer:
    def __init__(self, port, metric_name, metric_description):
        self.metric = Gauge(metric_name, metric_description)
        start_http_server(port)

    def update_metric(self, value):
        self.metric.set(value)
        print(f"Metric updated: {value}")
