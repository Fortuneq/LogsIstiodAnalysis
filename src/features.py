import re

# Каждая фича, должна сопровождаться timestamp, для дальнейшнего анализа
# Бинарные фичи - смотрим по регулярке наличие в строчке. При наличии - 1, иначе 0.
binary_features = [
    # Existing features
    {"Feature_name": "Context_error", "RegEx": r"Canceled desc = context canceled"},
    {"Feature_name": "x-b3-spanid", "RegEx": r"x-b3-spanid"},
    {"Feature_name": "x-b3-sampled", "RegEx": r"x-b3-sampled"},
    {"Feature_name": "x-b3-traceid", "RegEx": r"x-b3-traceid"},
    {"Feature_name": "Context_error", "RegEx": r"Canceled desc = context canceled"},
    {"Feature_name": "Log_Level_Error", "RegEx": r"\bERROR\b"},
    {
        "Feature_name": "Service_Unavailable",
        "RegEx": r"service unavailable|unavailable service",
    },
    {
        "Feature_name": "Configuration_Error",
        "RegEx": r"configuration error|invalid configuration",
    },
    {
        "Feature_name": "Authentication_Failure",
        "RegEx": r"authentication failed|failed authentication",
    },
    {
        "Feature_name": "Connection_Timeout",
        "RegEx": r"connection timeout|timeout occurred",
    },
    {"Feature_name": "Proxy_Sync_Issue", "RegEx": r"proxy sync problem|sync issue"},
    {"Feature_name": "Network_Failure", "RegEx": r"network failure|failed to connect"},
    {"Feature_name": "ChainErrors", "RegEx": r"buildSidecarOutboundListeners"},
    {"Feature_name": "TLS_Error", "RegEx": r"TLS handshake error|TLS error"},
    {
        "Feature_name": "Certificate_Error",
        "RegEx": r"certificate error|invalid certificate",
    },
    {"Feature_name": "RBAC_Permission_Denied", "RegEx": r"RBAC: access denied"},
    {
        "Feature_name": "Invalid_Token",
        "RegEx": r"invalid token|token validation failed",
    },
    {
        "Feature_name": "Routing_Error",
        "RegEx": r"routing error|invalid route configuration",
    },
    {
        "Feature_name": "Health_Check_Failure",
        "RegEx": r"health check failed|unhealthy endpoint",
    },
    {
        "Feature_name": "Database_Connection_Error",
        "RegEx": r"database connection error|DB connection failed",
    },
    {
        "Feature_name": "API_Server_Communication_Error",
        "RegEx": r"API server communication error|failed to communicate with API server",
    }
    # Добавьте по аналогии другие бинарные фичи, которые вам необходимы
]

numerical_features = [
    # CDS features
    {"Feature_name": "CDS_Clusters", "RegEx": r"CDS.*node:.+?clusters:(\d+)"},
    {"Feature_name": "CDS_Services", "RegEx": r"CDS.*node:.+?services:(\d+)"},
    # EDS features
    {"Feature_name": "EDS_Clusters", "RegEx": r"EDS.*node:.+?clusters:(\d+)"},
    {"Feature_name": "EDS_Endpoints", "RegEx": r"EDS.*node:.+?endpoints:(\d+)"},
    {"Feature_name": "EDS_Empty", "RegEx": r"EDS.*node:.+?empty:(\d+)"},
    # LDS features
    {"Feature_name": "LDS_Listeners", "RegEx": r"LDS.*node:.+?listeners:(\d+)"},
    # RDS features
    {"Feature_name": "RDS_Routes", "RegEx": r"RDS.*node:.+?routes:(\d+)"},
    # Объединенные данные из логов IstioD
]
