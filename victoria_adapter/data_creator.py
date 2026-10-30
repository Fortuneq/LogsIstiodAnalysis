import requests
import json
import time
import schedule


def send_log_to_loki(loki_url, log_data, labels):
    entries = []
    for log_line in log_data:
        # Генерация временной метки в наносекундах
        timestamp_ns = str(int(time.time() * 1e9))
        entries.append([timestamp_ns, log_line])

    payload = {"streams": [{"stream": labels, "values": entries}]}
    json_payload = json.dumps(payload)
    headers = {"Content-Type": "application/json"}
    response = requests.post(loki_url, data=json_payload, headers=headers)
    if response.status_code != 204:
        print(f"Ошибка при отправке лога: {response.status_code} - {response.text}")


def read_log_file(file_path, last_read_line, lines_to_read):
    with open(file_path, "r") as file:
        # Пропускаем строки, которые уже были прочитаны
        for _ in range(last_read_line):
            next(file)

        lines = []
        for _ in range(lines_to_read):
            line = file.readline()
            if not line:
                break  # Конец файла
            lines.append(line.strip())

    return lines, last_read_line + len(lines)


def send_logs_from_file_to_loki(file_path, loki_url, labels, state):
    log_data, state["last_read_line"] = read_log_file(
        file_path, state["last_read_line"], state["lines_to_read"]
    )
    print("DATA ADDED!")
    if log_data:
        send_log_to_loki(loki_url, log_data, labels)


loki_url = "http://localhost:3100/loki/api/v1/push"
labels = {"job": "your_job_name", "source": "your_source"}
file_path = "logs/istiod-discovery.log"  # Путь к файлу с логами
state = {"last_read_line": 0, "lines_to_read": 5000}

# Настройка планировщика для выполнения задачи каждую минуту
schedule.every(10).seconds.do(
    send_logs_from_file_to_loki, file_path, loki_url, labels, state
)

while True:
    schedule.run_pending()
    time.sleep(1)
