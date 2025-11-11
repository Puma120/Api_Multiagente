from agentes.base_agent import BaseAgent
from typing import Dict, Any, List
from config import GEMINI_MODELS
from sqlalchemy.orm import Session
from models import Transaccion, Presupuesto, Usuario, TipoTransaccion
from datetime import datetime, timedelta
import json

class EjecutorAgent(BaseAgent):
    """
    Agente Ejecutor: Realiza cálculos y operaciones financieras
    Usa protocolo ACP (Agent Communication Protocol) para intercambio estructurado
    """
    
    def __init__(self):
        super().__init__(
            name="Ejecutor",
            model_name=GEMINI_MODELS["ejecutor"],
            role="Ejecutar cálculos y operaciones financieras"
        )
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesar mensajes recibidos
        """
        msg_type = message.get("type")
        content = message.get("content")
        
        if msg_type == "EXECUTE_TASK":
            return self.execute_financial_task(content)
        elif msg_type == "CALCULATE":
            return self.perform_calculation(content)
        else:
            return {"status": "unknown_message_type", "type": msg_type}
    
    def execute_financial_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecutar tarea financiera específica
        """
        task_type = task.get("tipo")
        
        if task_type == "calcular_balance":
            return self.calculate_balance(task)
        elif task_type == "verificar_presupuestos":
            return self.verify_budgets(task)
        elif task_type == "analizar_gastos":
            return self.analyze_expenses(task)
        else:
            return {"status": "unknown_task_type", "task_type": task_type}
    
    def calculate_balance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcular balance financiero del usuario
        Usa ACP para comunicación estructurada con Knowledge Base
        """
        usuario_id = task.get("usuario_id")
        periodo_dias = task.get("periodo_dias", 30)
        
        # Enviar mensaje a Knowledge Base para obtener transacciones
        message_to_kb = self.send_message(
            to_agent="KnowledgeBase",
            protocol="ACP",
            message_type="QUERY_TRANSACTIONS",
            content={
                "usuario_id": usuario_id,
                "periodo_dias": periodo_dias
            }
        )
        
        # Simular respuesta (en implementación real vendría de KB)
        prompt = f"""
        Analiza el balance financiero:
        - Usuario ID: {usuario_id}
        - Período: últimos {periodo_dias} días
        
        Calcula y explica:
        1. Total de ingresos
        2. Total de gastos
        3. Balance neto
        4. Tendencia financiera
        
        Devuelve un JSON con:
        {{
            "ingresos_totales": 0.0,
            "gastos_totales": 0.0,
            "balance": 0.0,
            "analisis": "análisis detallado"
        }}
        """
        
        response = self.generate_with_ai(prompt, temperature=0.3)
        
        try:
            resultado = json.loads(response)
        except:
            resultado = {
                "ingresos_totales": 0.0,
                "gastos_totales": 0.0,
                "balance": 0.0,
                "analisis": response
            }
        
        return {
            "status": "balance_calculated",
            "resultado": resultado,
            "protocol_used": "ACP"
        }
    
    def verify_budgets(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verificar estado de presupuestos
        """
        usuario_id = task.get("usuario_id")
        
        prompt = f"""
        Verifica los presupuestos del usuario {usuario_id}.
        
        Para cada categoría de gasto, determina:
        1. Presupuesto asignado
        2. Monto gastado
        3. Porcentaje utilizado
        4. Estado (dentro/cerca/excedido)
        
        Devuelve JSON:
        {{
            "presupuestos": [
                {{"categoria": "alimentacion", "limite": 5000, "gastado": 3800, "porcentaje": 76, "estado": "cerca"}}
            ],
            "recomendaciones": ["recomendación 1", "recomendación 2"]
        }}
        """
        
        response = self.generate_with_ai(prompt, temperature=0.4)
        
        try:
            resultado = json.loads(response)
        except:
            resultado = {
                "presupuestos": [],
                "recomendaciones": ["Revisar gastos periódicamente"],
                "analisis_ia": response
            }
        
        # Si hay presupuestos cerca del límite, notificar
        for presupuesto in resultado.get("presupuestos", []):
            if presupuesto.get("porcentaje", 0) >= 80:
                self.send_message(
                    to_agent="Notificador",
                    protocol="A2A",
                    message_type="ALERT_REQUIRED",
                    content={
                        "usuario_id": usuario_id,
                        "tipo": "presupuesto_excedido",
                        "datos": presupuesto
                    }
                )
        
        return {
            "status": "budgets_verified",
            "resultado": resultado,
            "protocol_used": "ACP"
        }
    
    def analyze_expenses(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analizar patrones de gastos
        """
        usuario_id = task.get("usuario_id")
        
        prompt = f"""
        Analiza los patrones de gasto del usuario {usuario_id}.
        
        Identifica:
        1. Categorías con mayor gasto
        2. Tendencias de gasto
        3. Gastos inusuales o atípicos
        4. Oportunidades de ahorro
        
        Devuelve JSON con análisis detallado.
        """
        
        response = self.generate_with_ai(prompt, temperature=0.5)
        
        return {
            "status": "expenses_analyzed",
            "analisis": response,
            "protocol_used": "ACP"
        }
    
    def perform_calculation(self, calc: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realizar cálculo específico
        """
        calc_type = calc.get("type")
        data = calc.get("data")
        
        # Usar IA para cálculos complejos
        prompt = f"""
        Realiza el siguiente cálculo financiero:
        Tipo: {calc_type}
        Datos: {json.dumps(data)}
        
        Proporciona resultado numérico y explicación.
        """
        
        response = self.generate_with_ai(prompt, temperature=0.2)
        
        return {
            "status": "calculation_completed",
            "resultado": response
        }
