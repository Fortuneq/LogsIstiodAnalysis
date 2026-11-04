To run:

1. Start the log storage Docker container (Grafana Loki).
   docker run -d -p 3100:3100 grafana/loki:latest

2. For convenience and testing, upload data with a Python script using the requests library.
   python data_creator.py

3. Set the timestamp in the scheduler correctly so that it matches the data in the logs.
