from agentes.base_agent import BaseAgent
from typing import Dict, Any, List, Optional
from config import GEMINI_MODELS
from sqlalchemy.orm import Session
from models import Transaccion, Presupuesto, Usuario, AnalisisFinanciero
from datetime import datetime, timedelta
import json

class KnowledgeBaseAgent(BaseAgent):
    """
    Agente Base de Conocimiento: Almacena y proporciona datos históricos
    Usa protocolo MCP (Message Content Protocol) para estandarizar contenido
    """
    
    def __init__(self):
        super().__init__(
            name="KnowledgeBase",
            model_name=GEMINI_MODELS["knowledge_base"],
            role="Almacenar y proporcionar información financiera histórica"
        )
    
    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesar mensajes recibidos
        """
        msg_type = message.get("type")
        content = message.get("content")
        
        if msg_type == "QUERY_TRANSACTIONS":
            return self.query_transactions(content)
        elif msg_type == "QUERY_BUDGETS":
            return self.query_budgets(content)
        elif msg_type == "QUERY_HISTORICAL":
            return self.query_historical_data(content)
        elif msg_type == "STORE_ANALYSIS":
            return self.store_analysis(content)
        else:
            return {"status": "unknown_message_type", "type": msg_type}
    
    def query_transactions(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Consultar transacciones con filtros
        Usa MCP para estandarizar formato de respuesta
        """
        usuario_id = query.get("usuario_id")
        periodo_dias = query.get("periodo_dias", 30)
        categoria = query.get("categoria")
        tipo = query.get("tipo")
        
        # En implementación real, consultaría la base de datos
        # Aquí generamos respuesta estructurada usando MCP
        
        mcp_response = {
            "message_id": f"KB_{datetime.utcnow().timestamp()}",
            "protocol": "MCP",
            "content_type": "transaction_query_result",
            "data": {
                "usuario_id": usuario_id,
                "periodo": {
                    "inicio": (datetime.utcnow() - timedelta(days=periodo_dias)).isoformat(),
                    "fin": datetime.utcnow().isoformat()
                },
                "transacciones": [],  # Aquí irían las transacciones reales
                "total_count": 0,
                "filters_applied": {
                    "categoria": categoria,
                    "tipo": tipo
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return {
            "status": "query_completed",
            "result": mcp_response,
            "protocol_used": "MCP"
        }
    
    def query_budgets(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Consultar presupuestos
        """
        usuario_id = query.get("usuario_id")
        mes = query.get("mes", datetime.utcnow().month)
        anio = query.get("anio", datetime.utcnow().year)
        
        mcp_response = {
            "message_id": f"KB_{datetime.utcnow().timestamp()}",
            "protocol": "MCP",
            "content_type": "budget_query_result",
            "data": {
                "usuario_id": usuario_id,
                "periodo": {"mes": mes, "anio": anio},
                "presupuestos": [],  # Aquí irían los presupuestos reales
                "total_asignado": 0.0,
                "total_gastado": 0.0
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return {
            "status": "query_completed",
            "result": mcp_response,
            "protocol_used": "MCP"
        }
    
    def query_historical_data(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Consultar datos históricos con análisis de patrones
        """
        usuario_id = query.get("usuario_id")
        meses_atras = query.get("meses_atras", 6)
        
        prompt = f"""
        Analiza los patrones históricos financieros del usuario {usuario_id}:
        
        Período: últimos {meses_atras} meses
        
        Identifica:
        1. Patrones de gasto recurrentes
        2. Tendencias de ingreso
        3. Cambios significativos
        4. Predicciones para próximo período
        
        Devuelve JSON:
        {{
            "patrones_gasto": {{}},
            "tendencias_ingreso": {{}},
            "anomalias": [],
            "predicciones": {{}}
        }}
        """
        
        response = self.generate_with_ai(prompt, temperature=0.4)
        
        try:
            analisis = json.loads(response)
        except:
            analisis = {
                "patrones_gasto": {},
                "tendencias_ingreso": {},
                "anomalias": [],
                "predicciones": {},
                "analisis_ia": response
            }
        
        mcp_response = {
            "message_id": f"KB_{datetime.utcnow().timestamp()}",
            "protocol": "MCP",
            "content_type": "historical_analysis",
            "data": analisis,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return {
            "status": "historical_analysis_completed",
            "result": mcp_response,
            "protocol_used": "MCP"
        }
    
    def store_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Almacenar análisis financiero
        """
        usuario_id = analysis.get("usuario_id")
        tipo_analisis = analysis.get("tipo")
        datos = analysis.get("datos")
        
        # En implementación real, guardaría en base de datos
        
        mcp_response = {
            "message_id": f"KB_{datetime.utcnow().timestamp()}",
            "protocol": "MCP",
            "content_type": "storage_confirmation",
            "data": {
                "stored": True,
                "usuario_id": usuario_id,
                "tipo": tipo_analisis,
                "stored_at": datetime.utcnow().isoformat()
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return {
            "status": "analysis_stored",
            "result": mcp_response,
            "protocol_used": "MCP"
        }
    
    def get_spending_insights(self, usuario_id: int, categoria: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtener insights de gastos usando IA
        """
        prompt = f"""
        Proporciona insights inteligentes sobre los gastos del usuario {usuario_id}:
        
        {"Enfocado en categoría: " + categoria if categoria else "Todas las categorías"}
        
        Genera:
        1. Top 3 insights más importantes
        2. Comparación con promedios
        3. Sugerencias de optimización
        4. Alertas tempranas
        
        Formato JSON.
        """
        
        response = self.generate_with_ai(prompt, temperature=0.5)
        
        try:
            insights = json.loads(response)
        except:
            insights = {
                "insights": ["Mantener registro regular de gastos"],
                "comparaciones": {},
                "sugerencias": ["Revisar gastos mensuales"],
                "alertas": []
            }
        
        return {
            "status": "insights_generated",
            "insights": insights
        }
    
    def predict_future_expenses(self, usuario_id: int, meses_futuros: int = 3) -> Dict[str, Any]:
        """
        Predecir gastos futuros basado en histórico
        """
        prompt = f"""
        Predice los gastos futuros del usuario {usuario_id} para los próximos {meses_futuros} meses.
        
        Basado en:
        - Patrones históricos
        - Estacionalidad
        - Tendencias recientes
        
        Devuelve predicciones con intervalos de confianza.
        Formato JSON.
        """
        
        response = self.generate_with_ai(prompt, temperature=0.3)
        
        return {
            "status": "prediction_completed",
            "prediccion": response,
            "meses_futuros": meses_futuros
        }
