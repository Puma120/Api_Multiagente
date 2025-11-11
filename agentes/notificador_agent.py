from agentes.base_agent import BaseAgent
from typing import Dict, Any, List
from config import GEMINI_MODELS, FINANCE_CONFIG
from datetime import datetime
import json

class NotificadorAgent(BaseAgent):
    """
    Agente Notificador: Envía alertas y notificaciones sobre estado financiero
    Usa protocolo A2A (Agent-to-Agent) para comunicación general
    """
    
    def __init__(self):
        super().__init__(
            name="Notificador",
            model_name=GEMINI_MODELS["notificador"],
            role="Generar y enviar alertas financieras"
        )
        self.alert_threshold = FINANCE_CONFIG["alert_threshold_percentage"]
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesar mensajes recibidos
        """
        msg_type = message.get("type")
        content = message.get("content")
        
        if msg_type == "ALERT_REQUIRED":
            return self.create_alert(content)
        elif msg_type == "GENERATE_NOTIFICATION":
            return self.generate_notification(content)
        else:
            return {"status": "unknown_message_type", "type": msg_type}
    
    def create_alert(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear alerta basada en condiciones financieras
        Usa A2A para comunicación con otros agentes
        """
        usuario_id = alert_data.get("usuario_id")
        tipo = alert_data.get("tipo")
        datos = alert_data.get("datos", {})
        
        # Generar contenido de alerta usando IA
        prompt = f"""
        Genera una alerta financiera clara y concisa:
        
        Tipo de alerta: {tipo}
        Datos: {json.dumps(datos, indent=2)}
        
        La alerta debe:
        1. Tener un título claro (máximo 100 caracteres)
        2. Un mensaje explicativo (máximo 300 caracteres)
        3. Determinar nivel de severidad: "info", "warning", o "critical"
        4. Incluir recomendación de acción
        
        Devuelve JSON:
        {{
            "titulo": "título de la alerta",
            "mensaje": "mensaje detallado",
            "nivel": "warning",
            "recomendacion": "acción sugerida"
        }}
        """
        
        response = self.generate_with_ai(prompt, temperature=0.6)
        
        try:
            alerta = json.loads(response)
        except:
            alerta = {
                "titulo": f"Alerta: {tipo}",
                "mensaje": response[:300],
                "nivel": "warning",
                "recomendacion": "Revisar situación financiera"
            }
        
        # Enviar alerta a Interfaz usando AGUI
        self.send_message(
            to_agent="Interfaz",
            protocol="AGUI",
            message_type="DISPLAY_ALERT",
            content={
                "usuario_id": usuario_id,
                "alerta": alerta,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return {
            "status": "alert_created",
            "alerta": alerta,
            "protocol_used": "A2A"
        }
    
    def generate_notification(self, notif_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generar notificación informativa
        """
        usuario_id = notif_data.get("usuario_id")
        evento = notif_data.get("evento")
        contexto = notif_data.get("contexto", {})
        
        prompt = f"""
        Genera una notificación amigable para el usuario:
        
        Evento: {evento}
        Contexto: {json.dumps(contexto)}
        
        La notificación debe ser positiva, motivadora y útil.
        Máximo 200 caracteres.
        """
        
        response = self.generate_with_ai(prompt, temperature=0.7)
        
        notificacion = {
            "tipo": "info",
            "mensaje": response,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return {
            "status": "notification_generated",
            "notificacion": notificacion
        }
    
    def check_budget_alerts(self, presupuestos: List[Dict[str, Any]], usuario_id: int) -> List[Dict[str, Any]]:
        """
        Verificar si hay presupuestos que requieren alertas
        """
        alertas = []
        
        for presupuesto in presupuestos:
            porcentaje = (presupuesto.get("gastado", 0) / presupuesto.get("limite", 1)) * 100
            
            if porcentaje >= self.alert_threshold:
                alerta = self.create_alert({
                    "usuario_id": usuario_id,
                    "tipo": "presupuesto_cerca_limite",
                    "datos": {
                        "categoria": presupuesto.get("categoria"),
                        "porcentaje": porcentaje,
                        "gastado": presupuesto.get("gastado"),
                        "limite": presupuesto.get("limite")
                    }
                })
                alertas.append(alerta)
        
        return alertas
    
    def send_savings_recommendation(self, usuario_id: int, analisis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enviar recomendación de ahorro basada en análisis
        """
        prompt = f"""
        Basado en el siguiente análisis financiero, genera una recomendación de ahorro:
        
        {json.dumps(analisis, indent=2)}
        
        La recomendación debe:
        1. Ser específica y accionable
        2. Considerar el contexto del usuario
        3. Ser motivadora
        4. Incluir metas realistas
        
        Devuelve mensaje de máximo 250 caracteres.
        """
        
        response = self.generate_with_ai(prompt, temperature=0.7)
        
        return self.generate_notification({
            "usuario_id": usuario_id,
            "evento": "recomendacion_ahorro",
            "contexto": {"mensaje": response}
        })
