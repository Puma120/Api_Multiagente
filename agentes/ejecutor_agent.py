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
        Calcular balance financiero del usuario con datos reales
        Usa ACP para comunicación estructurada
        """
        usuario_id = task.get("usuario_id")
        periodo_dias = task.get("periodo_dias", 30)
        datos_reales = task.get("datos_reales", {})
        tiene_datos = task.get("tiene_datos", False)
        
        if not tiene_datos:
            return {
                "status": "balance_calculated",
                "resultado": {
                    "ingresos_totales": 0.0,
                    "gastos_totales": 0.0,
                    "balance": 0.0,
                    "total_transacciones": 0,
                    "analisis": f"No hay transacciones registradas en los últimos {periodo_dias} días. Comienza a registrar tus ingresos y gastos para obtener análisis personalizados."
                },
                "protocol_used": "ACP"
            }
        
        # Enviar mensaje a Knowledge Base (protocolo ACP)
        self.send_message(
            to_agent="KnowledgeBase",
            protocol="ACP",
            message_type="QUERY_TRANSACTIONS",
            content={
                "usuario_id": usuario_id,
                "periodo_dias": periodo_dias
            }
        )
        
        # Preparar datos para análisis de IA
        datos_json = json.dumps(datos_reales, indent=2)
        
        prompt = f"""
        Analiza el balance financiero REAL del usuario {usuario_id} en los últimos {periodo_dias} días:

        DATOS REALES:
        {datos_json}

        Proporciona un análisis detallado que incluya:
        1. Evaluación del balance (positivo/negativo/equilibrado)
        2. Análisis de los gastos por categoría
        3. Comparación con el ingreso mensual declarado
        4. Identificación de categorías problemáticas
        5. Recomendaciones específicas para mejorar
        6. Tendencia financiera (ahorrando/gastando más de lo necesario)

        IMPORTANTE: Responde SOLO con un objeto JSON válido, sin formato markdown, sin bloques de código, sin ```json ni ```. Solo el JSON puro.

        Formato JSON requerido:
        {{
            "evaluacion_general": "descripción del estado financiero",
            "puntos_criticos": ["punto 1", "punto 2"],
            "recomendaciones": ["recomendación 1", "recomendación 2"],
            "tendencia": "positiva/negativa/estable"
        }}
        """
        
        response = self.generate_with_ai(prompt, temperature=0.3)
        
        try:
            analisis_ia = json.loads(response)
        except:
            analisis_ia = {
                "evaluacion_general": response,
                "puntos_criticos": [],
                "recomendaciones": ["Continúa monitoreando tus finanzas regularmente"],
                "tendencia": "estable"
            }
        
        # Combinar datos reales con análisis de IA
        resultado = {
            "ingresos_totales": datos_reales.get("ingresos_totales", 0.0),
            "gastos_totales": datos_reales.get("gastos_totales", 0.0),
            "balance": datos_reales.get("balance", 0.0),
            "total_transacciones": datos_reales.get("total_transacciones", 0),
            "gastos_por_categoria": datos_reales.get("gastos_por_categoria", {}),
            "analisis_ia": analisis_ia
        }
        
        return {
            "status": "balance_calculated",
            "resultado": resultado,
            "protocol_used": "ACP"
        }
    
    def verify_budgets(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verificar estado de presupuestos usando datos reales de la base de datos
        """
        usuario_id = task.get("usuario_id")
        presupuestos_reales = task.get("presupuestos_reales", [])
        tiene_datos = task.get("tiene_datos", False)
        
        if not tiene_datos or len(presupuestos_reales) == 0:
            return {
                "status": "budgets_verified",
                "resultado": {
                    "presupuestos": [],
                    "recomendaciones": [
                        "No hay presupuestos configurados para este mes.",
                        "Crea presupuestos para empezar a controlar tus gastos."
                    ],
                    "mensaje": "Usuario sin presupuestos activos"
                },
                "protocol_used": "ACP"
            }
        
        # Calcular estado de cada presupuesto
        presupuestos_analizados = []
        for p in presupuestos_reales:
            porcentaje = p.get("porcentaje", 0)
            
            # Determinar estado
            if porcentaje <= 75:
                estado = "dentro"
            elif porcentaje <= 100:
                estado = "cerca"
            else:
                estado = "excedido"
            
            presupuestos_analizados.append({
                "categoria": p.get("categoria"),
                "limite": p.get("limite"),
                "gastado": p.get("gastado"),
                "porcentaje": porcentaje,
                "estado": estado
            })
        
        # Preparar datos para análisis de IA
        datos_json = json.dumps(presupuestos_analizados, indent=2)
        
        prompt = f"""
        Analiza los siguientes presupuestos REALES del usuario {usuario_id}:

        {datos_json}

        Estados:
        - "dentro": <= 75% del presupuesto
        - "cerca": 76-100% del presupuesto  
        - "excedido": > 100% del presupuesto

        Proporciona:
        1. Análisis detallado de cada categoría
        2. Recomendaciones específicas basadas en los datos reales
        3. Consejos para optimizar gastos

        IMPORTANTE: Responde SOLO con un objeto JSON válido, sin formato markdown, sin bloques de código, sin ```json ni ```. Solo el JSON puro.

        Formato JSON requerido:
        {{
            "analisis_detallado": "análisis completo basado en datos reales",
            "recomendaciones": ["recomendación 1", "recomendación 2", "recomendación 3"]
        }}
        """
        
        response = self.generate_with_ai(prompt, temperature=0.4)
        
        try:
            analisis_ia = json.loads(response)
        except:
            analisis_ia = {
                "analisis_detallado": response,
                "recomendaciones": ["Mantén un seguimiento regular de tus gastos"]
            }
        
        # Notificar sobre presupuestos críticos
        for presupuesto in presupuestos_analizados:
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
            "resultado": {
                "presupuestos": presupuestos_analizados,
                "analisis_ia": analisis_ia.get("analisis_detallado", ""),
                "recomendaciones": analisis_ia.get("recomendaciones", [])
            },
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
