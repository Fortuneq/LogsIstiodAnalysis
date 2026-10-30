from dateutil import parser as dateutil_parser
from collections import defaultdict
import re


class IstioLogParser:
    def __init__(self, binary_features, numerical_features):
        self.binary_features = binary_features
        self.numerical_features = numerical_features

    def parse_line(self, line):
        binary_results = {
            feature["Feature_name"]: 0 for feature in self.binary_features
        }
        numerical_results = {
            feature["Feature_name"]: 0 for feature in self.numerical_features
        }
        # Обработка бинарных признаков
        for feature in self.binary_features:
            match = re.search(feature["RegEx"], line)
            if match:
                binary_results[feature["Feature_name"]] = 1

        # Обработка числовых признаков
        for feature in self.numerical_features:
            match = re.search(feature["RegEx"], line)
            if match:
                if feature["Feature_name"] == "IstioD_Request_Type":
                    numerical_results[feature["Feature_name"]] = match.group(1)
                else:
                    try:
                        numerical_results[feature["Feature_name"]] = float(
                            match.group(1)
                        )
                    except ValueError:
                        print(
                            f"Ошибка преобразования: {match.group(1)} не является числом"
                        )
                        continue  # Пропускаем добавление этого признака

        return binary_results, numerical_results

    def parse_logs(self, log_lines):
        aggregated_binary_results = defaultdict(int)
        aggregated_numerical_results = defaultdict(float)
        feature_line_indices = defaultdict(list)  # Словарь для хранения индексов строк

        cnt = 0
        for idx, line in enumerate(log_lines):
            binary_results, numerical_results = self.parse_line(line)

            # Агрегация бинарных и числовых признаков
            for feature, value in binary_results.items():
                aggregated_binary_results[feature] += value
                if value:  # Если признак активен, сохраняем индекс строки
                    feature_line_indices[feature].append(idx)

            for feature, value in numerical_results.items():
                aggregated_numerical_results[feature] += value

            cnt += 1

        # Сохраняем строки с активированными признаками в файл
        self.save_feature_lines_to_file(log_lines, feature_line_indices)

        results = {
            "Context_error": 0,
            "x-b3-spanid": 0,
            "x-b3-sampled": 0,
            "x-b3-traceid": 0,
            "Log_Level_Error": 0,
            "Service_Unavailable": 0,
            "Configuration_Error": 0,
            "Authentication_Failure": 0,
            "Connection_Timeout": 0,
            "Proxy_Sync_Issue": 0,
            "Network_Failure": 0,
            "ChainErrors": 0,
            "TLS_Error": 0,
            "Certificate_Error": 0,
            "RBAC_Permission_Denied": 0,
            "Invalid_Token": 0,
            "Routing_Error": 0,
            "Health_Check_Failure": 0,
            "Database_Connection_Error": 0,
            "API_Server_Communication_Error": 0,
            "CDS_Clusters": 0,
            "CDS_Services": 0,
            "EDS_Clusters": 0,
            "EDS_Endpoints": 0,
            "EDS_Empty": 0,
            "LDS_Listeners": 0,
            "RDS_Routes": 0,
        }
        for feature_dict in [aggregated_binary_results, aggregated_numerical_results]:
            for feature in feature_dict:
                results[feature] = feature_dict[feature] / cnt if cnt > 0 else 0
        print(results)
        return list(results.values())

    def save_feature_lines_to_file(self, log_lines, feature_line_indices):
        with open("../postgres_adapter/feature_lines.txt", "w") as file:
            for feature, indices in feature_line_indices.items():
                file.write(f"{feature}:\n")
                for idx in indices:
                    file.write(f"\tindex_{idx}: {log_lines[idx]}\n")
                file.write("\n")
