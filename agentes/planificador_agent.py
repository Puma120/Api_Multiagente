from agentes.base_agent import BaseAgent
from typing import Dict, Any, List
from config import GEMINI_MODELS
import json

class PlanificadorAgent(BaseAgent):
    """
    Agente Planificador: Descompone tareas financieras en subtareas
    Usa protocolo ANP (Agent Negotiation Protocol) para distribuir tareas
    """
    
    def __init__(self):
        super().__init__(
            name="Planificador",
            model_name=GEMINI_MODELS["planificador"],
            role="Descomponer tareas financieras en subtareas y coordinar agentes"
        )
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesar mensajes recibidos
        """
        msg_type = message.get("type")
        content = message.get("content")
        
        if msg_type == "REQUEST_PLAN":
            return self.create_financial_plan(content)
        elif msg_type == "TASK_COMPLETED":
            return self.handle_task_completion(content)
        else:
            return {"status": "unknown_message_type", "type": msg_type}
    
    def create_financial_plan(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear plan financiero desglosado en subtareas
        Usa ANP (Agent Negotiation Protocol) para negociar distribución de tareas
        """
        usuario_id = request.get("usuario_id")
        objetivo = request.get("objetivo", "analizar_finanzas")
        
        prompt = f"""
        Eres un planificador financiero experto. Descompón la siguiente tarea en subtareas específicas:
        
        Objetivo: {objetivo}
        Usuario ID: {usuario_id}
        
        AGENTES DISPONIBLES (usa EXACTAMENTE estos nombres):
        - Ejecutor: Realiza cálculos financieros, balances, verificación de presupuestos
        - KnowledgeBase: Consulta datos históricos, transacciones, patrones de gasto
        - Notificador: Genera alertas y notificaciones al usuario
        - Interfaz: Formatea datos para presentación al usuario
        - Monitor: Supervisa el sistema y métricas
        
        TIPOS DE TAREAS VÁLIDOS:
        Para Ejecutor: calcular_balance, verificar_presupuestos, analizar_gastos
        Para KnowledgeBase: recopilar_transacciones, analizar_patrones, consultar_historico
        Para Notificador: generar_alertas, enviar_notificaciones
        Para Interfaz: formatear_reporte, crear_dashboard
        Para Monitor: registrar_actividad, monitorear_sistema
        
        IMPORTANTE: 
        1. Usa SOLO los nombres de agentes listados arriba (exactamente como aparecen)
        2. Cada subtarea debe asignarse a UN agente existente
        3. Responde SOLO con un objeto JSON válido, sin markdown, sin ```json
        
        Formato JSON requerido:
        {{
            "subtareas": [
                {{"id": 1, "tipo": "calcular_balance", "descripcion": "Calcular balance financiero del usuario", "agente": "Ejecutor", "prioridad": "alta"}},
                {{"id": 2, "tipo": "recopilar_transacciones", "descripcion": "Obtener historial de transacciones", "agente": "KnowledgeBase", "prioridad": "alta"}},
                {{"id": 3, "tipo": "generar_alertas", "descripcion": "Generar alertas si hay anomalías", "agente": "Notificador", "prioridad": "media"}}
            ],
            "estrategia": "descripción de la estrategia general"
        }}
        """
        
        response = self.generate_with_ai(prompt, temperature=0.5)
        
        try:
            # Intentar parsear la respuesta como JSON
            plan = json.loads(response)
        except:
            # Si falla, crear plan básico
            plan = {
                "subtareas": [
                    {"id": 1, "tipo": "calcular_balance", "descripcion": "Calcular balance actual", "agente": "Ejecutor", "prioridad": "alta"},
                    {"id": 2, "tipo": "verificar_presupuestos", "descripcion": "Verificar estado de presupuestos", "agente": "Ejecutor", "prioridad": "media"},
                    {"id": 3, "tipo": "generar_alertas", "descripcion": "Generar alertas si es necesario", "agente": "Notificador", "prioridad": "media"}
                ],
                "estrategia": "Análisis financiero estándar",
                "respuesta_ia": response
            }
        
        # Enviar subtareas a los agentes correspondientes usando ANP
        # Distribuir cada subtarea al agente indicado en el plan
        subtareas = plan.get("subtareas", []) if isinstance(plan, dict) else []
        task_results = []
        for tarea in subtareas:
            agente_destino = tarea.get("agente")
            if agente_destino:
                # Enviar ejecución de tarea al agente destino y recoger respuesta
                response = self.send_message(
                    to_agent=agente_destino,
                    protocol="ANP",
                    message_type="EXECUTE_TASK",
                    content={
                        "task": tarea,
                        "plan_estrategia": plan.get("estrategia") if isinstance(plan, dict) else None,
                        "context": request
                    }
                )
                task_results.append({"tarea": tarea, "response": response})

        # También notificar al Monitor sobre la distribución
        self.send_message(
            to_agent="Monitor",
            protocol="ANP",
            message_type="TASK_DISTRIBUTION",
            content=plan
        )
        
        return {
            "status": "plan_created",
            "plan": plan,
            "task_results": task_results,
            "protocol_used": "ANP"
        }
    
    def handle_task_completion(self, completion: Dict[str, Any]) -> Dict[str, Any]:
        """
        Manejar la finalización de una subtarea
        """
        task_id = completion.get("task_id")
        resultado = completion.get("resultado")
        
        return {
            "status": "task_completion_acknowledged",
            "task_id": task_id,
            "next_step": "continue_execution"
        }
    
    def plan_budget_analysis(self, usuario_id: int, mes: int, anio: int) -> Dict[str, Any]:
        """
        Planificar análisis de presupuesto mensual
        """
        return self.create_financial_plan({
            "usuario_id": usuario_id,
            "objetivo": f"analizar_presupuesto_mensual_{mes}_{anio}"
        })
    
    def plan_savings_strategy(self, usuario_id: int, objetivo_ahorro: float) -> Dict[str, Any]:
        """
        Planificar estrategia de ahorro
        """
        return self.create_financial_plan({
            "usuario_id": usuario_id,
            "objetivo": f"crear_estrategia_ahorro_{objetivo_ahorro}"
        })
