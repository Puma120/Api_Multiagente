from agentes.base_agent import BaseAgent
from typing import Dict, Any, List
from config import GEMINI_MODELS
import json

class InterfazAgent(BaseAgent):
    """
    Agente Interfaz: Formatea y presenta información al usuario
    Usa protocolo AGUI (Agent-to-User Interface) para comunicación con UI
    """
    
    def __init__(self):
        super().__init__(
            name="Interfaz",
            model_name=GEMINI_MODELS["interfaz"],
            role="Formatear y presentar información al usuario"
        )
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesar mensajes recibidos
        """
        msg_type = message.get("type")
        content = message.get("content")
        
        if msg_type == "DISPLAY_ALERT":
            return self.format_alert_for_ui(content)
        elif msg_type == "DISPLAY_ANALYSIS":
            return self.format_analysis_for_ui(content)
        elif msg_type == "DISPLAY_DASHBOARD":
            return self.create_dashboard(content)
        else:
            return {"status": "unknown_message_type", "type": msg_type}
    
    def format_alert_for_ui(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formatear alerta para presentación en UI
        Usa AGUI para comunicación con interfaz de usuario
        """
        usuario_id = alert_data.get("usuario_id")
        alerta = alert_data.get("alerta", {})
        
        # Formatear con estilo apropiado según nivel
        nivel = alerta.get("nivel", "info")
        
        ui_alert = {
            "tipo": "alerta",
            "nivel": nivel,
            "titulo": alerta.get("titulo", "Notificación"),
            "mensaje": alerta.get("mensaje", ""),
            "recomendacion": alerta.get("recomendacion"),
            "timestamp": alert_data.get("timestamp"),
            "estilo": self._get_alert_style(nivel),
            "accion_sugerida": self._get_suggested_action(nivel)
        }
        
        return {
            "status": "alert_formatted",
            "ui_data": ui_alert,
            "protocol_used": "AGUI"
        }
    
    def format_analysis_for_ui(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formatear análisis financiero para UI
        """
        usuario_id = analysis_data.get("usuario_id")
        analisis = analysis_data.get("analisis", {})
        
        prompt = f"""
        Transforma el siguiente análisis financiero en un formato amigable para el usuario:
        
        {json.dumps(analisis, indent=2)}
        
        Crea:
        1. Un resumen ejecutivo (2-3 líneas)
        2. Puntos clave (3-5 bullets)
        3. Métricas destacadas (números importantes)
        4. Sugerencias de acción
        
        Devuelve JSON:
        {{
            "resumen": "texto del resumen",
            "puntos_clave": ["punto 1", "punto 2"],
            "metricas": {{"ingreso_total": 10000, "gasto_total": 7000}},
            "sugerencias": ["sugerencia 1", "sugerencia 2"]
        }}
        """
        
        response = self.generate_with_ai(prompt, temperature=0.6)
        
        try:
            ui_analysis = json.loads(response)
        except:
            ui_analysis = {
                "resumen": "Análisis financiero completado",
                "puntos_clave": ["Revisar resultados"],
                "metricas": analisis,
                "sugerencias": ["Mantener seguimiento regular"]
            }
        
        return {
            "status": "analysis_formatted",
            "ui_data": ui_analysis,
            "protocol_used": "AGUI"
        }
    
    def create_dashboard(self, dashboard_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear dashboard completo para el usuario
        """
        usuario_id = dashboard_data.get("usuario_id")
        datos = dashboard_data.get("datos", {})
        
        prompt = f"""
        Crea un dashboard financiero completo para el usuario:
        
        Datos disponibles:
        {json.dumps(datos, indent=2)}
        
        El dashboard debe incluir:
        1. Resumen financiero general
        2. Estado de presupuestos
        3. Alertas activas
        4. Tendencias recientes
        5. Recomendaciones principales
        
        Formato JSON estructurado para visualización.
        """
        
        response = self.generate_with_ai(prompt, temperature=0.5)
        
        try:
            dashboard = json.loads(response)
        except:
            dashboard = {
                "resumen": {"balance": 0, "ingresos": 0, "gastos": 0},
                "presupuestos": [],
                "alertas": [],
                "tendencias": "Sin datos suficientes",
                "recomendaciones": []
            }
        
        return {
            "status": "dashboard_created",
            "ui_data": dashboard,
            "protocol_used": "AGUI"
        }
    
    def _get_alert_style(self, nivel: str) -> Dict[str, str]:
        """
        Obtener estilo visual según nivel de alerta
        """
        styles = {
            "info": {"color": "blue", "icon": "ℹ️", "priority": "low"},
            "warning": {"color": "orange", "icon": "⚠️", "priority": "medium"},
            "critical": {"color": "red", "icon": "🚨", "priority": "high"}
        }
        return styles.get(nivel, styles["info"])
    
    def _get_suggested_action(self, nivel: str) -> str:
        """
        Obtener acción sugerida según nivel
        """
        actions = {
            "info": "Revisar cuando sea conveniente",
            "warning": "Revisar pronto",
            "critical": "Requiere atención inmediata"
        }
        return actions.get(nivel, "Revisar")
    
    def format_transaction_list(self, transacciones: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Formatear lista de transacciones para UI
        """
        prompt = f"""
        Formatea estas transacciones de manera clara y organizada:
        
        Total de transacciones: {len(transacciones)}
        
        Organiza por:
        1. Fecha (más recientes primero)
        2. Agrupa por categoría
        3. Destaca montos importantes
        4. Calcula totales por categoría
        
        Devuelve JSON estructurado para visualización.
        """
        
        response = self.generate_with_ai(prompt, temperature=0.4)
        
        return {
            "status": "transactions_formatted",
            "ui_data": response,
            "total": len(transacciones)
        }
