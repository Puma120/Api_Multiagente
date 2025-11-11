import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de PostgreSQL (Render)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://finanzas_zz74_user:OY8LbDEk5eUbY9qJWtuRwnTy956vEOV0@dpg-d498208dl3ps73fr5cq0-a.oregon-postgres.render.com/finanzas_zz74"
)

# Configuración de Google AI Studio
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Configuración de Modelos Gemini
GEMINI_MODELS = {
    "planificador": "gemini-2.0-flash",  # Rápido para planificación
    "ejecutor": "gemini-2.5-flash",      # Balance para cálculos
    "notificador": "gemini-2.0-flash",   # Rápido para alertas
    "interfaz": "gemini-2.0-flash",      # Rápido para UI
    "knowledge_base": "gemini-2.5-flash",  # Flash para análisis histórico
    "monitor": "gemini-2.0-flash"        # Rápido para supervisión
}

# Configuración de la aplicación
APP_NAME = "Sistema Multiagente de Finanzas Personales"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Configuración de Protocolos
PROTOCOLS_CONFIG = {
    "A2A": {
        "enabled": True,
        "description": "Agent-to-Agent: Comunicación general entre agentes"
    },
    "ACP": {
        "enabled": True,
        "description": "Agent Communication Protocol: Intercambio estructurado de mensajes"
    },
    "ANP": {
        "enabled": True,
        "description": "Agent Negotiation Protocol: Resolución de conflictos y distribución de tareas"
    },
    "AGUI": {
        "enabled": True,
        "description": "Agent-to-User Interface: Comunicación con la interfaz de usuario"
    },
    "MCP": {
        "enabled": True,
        "description": "Message Content Protocol: Semántica del contenido del mensaje"
    }
}

# Umbrales y configuraciones financieras
FINANCE_CONFIG = {
    "alert_threshold_percentage": 80,  # Alertar si se usa el 80% del presupuesto
    "savings_recommendation_rate": 0.2,  # Recomendar ahorrar 20%
    "max_transactions_per_query": 100,
    "analysis_period_days": 30
}
