Для работы:

1. Запустить докер-контейнер с Victoria metrics.
   docker run -d -p 3100:3100 grafana/loki:latest

2. Для удобства и тестирования для закачки данных в V.M будем использовать python-script и библиотеку requests.
   python data_creator.py

3. Правильно выставить временную метку в scheduler, которая соответствует данным в логах.
