from agentes.base_agent import BaseAgent
from typing import Dict, Any, List
from config import GEMINI_MODELS
from datetime import datetime
import json

class MonitorAgent(BaseAgent):
    """
    Agente Monitor: Supervisa el tráfico y estado de los agentes
    Usa múltiples protocolos para coordinación general
    """
    
    def __init__(self):
        super().__init__(
            name="Monitor",
            model_name=GEMINI_MODELS["monitor"],
            role="Supervisar tráfico y estado del sistema multiagente"
        )
        self.agent_status = {}
        self.message_queue = []
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesar mensajes recibidos
        """
        msg_type = message.get("type")
        content = message.get("content")
        
        if msg_type == "TASK_DISTRIBUTION":
            return self.monitor_task_distribution(content)
        elif msg_type == "AGENT_STATUS":
            return self.update_agent_status(content)
        elif msg_type == "SYSTEM_HEALTH_CHECK":
            return self.check_system_health()
        elif msg_type == "EXECUTE_TASK":
            # Soporte para tareas del Planificador
            task = content.get("task") if isinstance(content, dict) else None
            if task and task.get("tipo") in ["registrar_actividad", "monitorear_sistema"]:
                return self.check_system_health()
            return {"status": "task_executed", "task": task}
        else:
            return {"status": "unknown_message_type", "type": msg_type}
    
    def monitor_task_distribution(self, distribution: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitorear distribución de tareas entre agentes
        """
        subtareas = distribution.get("subtareas", [])
        estrategia = distribution.get("estrategia")
        
        # Registrar distribución
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "tipo": "task_distribution",
            "total_tareas": len(subtareas),
            "estrategia": estrategia,
            "agentes_involucrados": list(set([t.get("agente") for t in subtareas]))
        }
        
        self.message_queue.append(log_entry)
        
        # Analizar carga de trabajo
        prompt = f"""
        Analiza la distribución de tareas:
        
        {json.dumps(distribution, indent=2)}
        
        Determina:
        1. Está balanceada la carga?
        2. Hay cuellos de botella potenciales?
        3. Orden óptimo de ejecución
        4. Estimación de tiempo total
        
        Devuelve JSON con análisis y recomendaciones.
        """
        
        response = self.generate_with_ai(prompt, temperature=0.4)
        
        try:
            analisis = json.loads(response)
        except:
            analisis = {
                "balanceada": True,
                "cuellos_botella": [],
                "orden_sugerido": subtareas,
                "estimacion_minutos": 5
            }
        
        return {
            "status": "distribution_monitored",
            "analisis": analisis,
            "log_entry": log_entry
        }
    
    def update_agent_status(self, status: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar estado de un agente
        """
        agent_name = status.get("agent_name")
        estado = status.get("estado")
        
        self.agent_status[agent_name] = {
            "estado": estado,
            "ultima_actualizacion": datetime.utcnow().isoformat(),
            "metadata": status.get("metadata", {})
        }
        
        return {
            "status": "agent_status_updated",
            "agent": agent_name,
            "estado": estado
        }
    
    def check_system_health(self) -> Dict[str, Any]:
        """
        Verificar salud general del sistema
        """
        prompt = f"""
        Evalúa la salud del sistema multiagente:
        
        Estados de agentes:
        {json.dumps(self.agent_status, indent=2)}
        
        Cola de mensajes: {len(self.message_queue)} mensajes
        
        Determina:
        1. Estado general del sistema (healthy/degraded/critical)
        2. Agentes con problemas
        3. Recomendaciones de optimización
        4. Alertas necesarias
        
        Devuelve JSON.
        """
        
        response = self.generate_with_ai(prompt, temperature=0.3)
        
        try:
            health = json.loads(response)
        except:
            health = {
                "estado_general": "healthy",
                "agentes_problema": [],
                "recomendaciones": ["Sistema operando normalmente"],
                "alertas": []
            }
        
        return {
            "status": "health_check_completed",
            "health": health,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """
        Obtener métricas del sistema
        """
        total_messages = len(self.message_queue)
        active_agents = len([a for a, s in self.agent_status.items() if s.get("estado") == "active"])
        
        return {
            "total_mensajes": total_messages,
            "agentes_activos": active_agents,
            "agentes_total": len(self.agent_status),
            "ultima_actividad": datetime.utcnow().isoformat(),
            "cola_mensajes": self.message_queue[-10:]  # Últimos 10 mensajes
        }
    
    def analyze_communication_flow(self) -> Dict[str, Any]:
        """
        Analizar flujo de comunicación entre agentes
        """
        prompt = f"""
        Analiza el flujo de comunicación del sistema:
        
        Total de mensajes: {len(self.message_queue)}
        Agentes activos: {len(self.agent_status)}
        
        Identifica:
        1. Patrones de comunicación
        2. Eficiencia del flujo
        3. Posibles mejoras
        4. Protocolos más utilizados
        
        Devuelve análisis en JSON.
        """
        
        response = self.generate_with_ai(prompt, temperature=0.5)
        
        return {
            "status": "flow_analyzed",
            "analisis": response
        }
    
    def clear_message_queue(self):
        """
        Limpiar cola de mensajes
        """
        old_count = len(self.message_queue)
        self.message_queue = []
        
        return {
            "status": "queue_cleared",
            "messages_cleared": old_count
        }
