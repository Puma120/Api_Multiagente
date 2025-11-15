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
        elif msg_type == "EXECUTE_TASK":
            # Accept tasks dispatched by Planificador
            task = content.get("task") if isinstance(content, dict) else None
            context = content.get("context") if isinstance(content, dict) else None
            if not task:
                return {"status": "error", "error": "no_task_provided"}

            tipo = task.get("tipo")
            # If context provides real data, prefer returning that instead of querying DB
            if tipo == "analizar_patrones":
                meses = task.get("meses_atras", 6)
                if context and isinstance(context, dict) and context.get("datos_reales"):
                    # Use provided historical data if available
                    return {
                        "status": "historical_analysis_completed",
                        "result": {
                            "message_id": f"KB_{datetime.utcnow().timestamp()}",
                            "protocol": "MCP",
                            "content_type": "historical_analysis",
                            "data": context.get("datos_reales"),
                            "timestamp": datetime.utcnow().isoformat()
                        },
                        "protocol_used": "MCP"
                    }
                return self.query_historical_data({"usuario_id": task.get("usuario_id"), "meses_atras": meses})
            elif tipo == "recopilar_transacciones" or "transaccion" in tipo.lower() or "datos" in tipo.lower():
                if context and isinstance(context, dict) and context.get("datos_reales"):
                    return {
                        "status": "query_completed",
                        "result": {
                            "message_id": f"KB_{datetime.utcnow().timestamp()}",
                            "protocol": "MCP",
                            "content_type": "transaction_query_result",
                            "data": context.get("datos_reales"),
                            "timestamp": datetime.utcnow().isoformat()
                        },
                        "protocol_used": "MCP"
                    }
                return self.query_transactions({"usuario_id": task.get("usuario_id"), "periodo_dias": task.get("periodo_dias", 30)})
            elif tipo == "verificar_presupuestos" or "presupuesto" in tipo.lower():
                if context and isinstance(context, dict) and context.get("presupuestos_reales"):
                    return {
                        "status": "query_completed",
                        "result": {
                            "message_id": f"KB_{datetime.utcnow().timestamp()}",
                            "protocol": "MCP",
                            "content_type": "budget_query_result",
                            "data": {
                                "usuario_id": task.get("usuario_id"),
                                "periodo": {"mes": task.get("mes"), "anio": task.get("anio")},
                                "presupuestos": context.get("presupuestos_reales"),
                                "total_asignado": sum(p.get("limite", 0) for p in context.get("presupuestos_reales", [])),
                                "total_gastado": sum(p.get("gastado", 0) for p in context.get("presupuestos_reales", []))
                            },
                            "timestamp": datetime.utcnow().isoformat()
                        },
                        "protocol_used": "MCP"
                    }
                return self.query_budgets({"usuario_id": task.get("usuario_id"), "mes": task.get("mes"), "anio": task.get("anio")})
            elif tipo == "consultar_historico" or "histor" in tipo.lower():
                return self.query_historical_data({"usuario_id": task.get("usuario_id"), "meses_atras": task.get("meses_atras", 6)})
            else:
                # Default: return context data if available
                if context and isinstance(context, dict) and context.get("datos_reales"):
                    return {
                        "status": "query_completed",
                        "result": {
                            "message_id": f"KB_{datetime.utcnow().timestamp()}",
                            "protocol": "MCP",
                            "content_type": "generic_query_result",
                            "data": context.get("datos_reales"),
                            "timestamp": datetime.utcnow().isoformat()
                        },
                        "protocol_used": "MCP"
                    }
                return {"status": "unknown_task_type", "task_type": tipo}
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
    
    def get_spending_insights(self, usuario_id: int, categoria: Optional[str] = None, datos_reales: Optional[Dict] = None, tiene_datos: bool = False) -> Dict[str, Any]:
        """
        Obtener insights de gastos usando IA con datos reales
        """
        if not tiene_datos or not datos_reales:
            return {
                "status": "insights_generated",
                "insights": {
                    "insights": ["No hay datos suficientes para generar insights. Registra transacciones primero."],
                    "comparaciones": {},
                    "sugerencias": ["Comienza a registrar tus ingresos y gastos para obtener análisis personalizados"],
                    "alertas": []
                }
            }
        
        datos_json = json.dumps(datos_reales, indent=2)
        
        prompt = f"""
        Analiza los siguientes DATOS REALES del usuario {usuario_id}:
        
        {datos_json}
        
        {"Enfocado en categoría: " + categoria if categoria else "Análisis completo de todas las categorías"}
        
        Genera insights inteligentes basados en:
        1. Patrones reales de gasto por categoría
        2. Comparación de gastos vs ingresos
        3. Estado de presupuestos (si hay)
        4. Identificación de categorías problemáticas
        5. Oportunidades de ahorro específicas
        
        IMPORTANTE: Responde SOLO con un objeto JSON válido, sin formato markdown, sin bloques de código, sin ```json ni ```. Solo el JSON puro.
        
        Formato JSON requerido:
        {{
            "insights": ["insight 1 basado en datos reales", "insight 2", "insight 3"],
            "comparaciones": {{
                "gastos_vs_ingresos": "análisis comparativo",
                "categoria_mayor_gasto": "nombre de categoría"
            }},
            "sugerencias": ["sugerencia específica 1", "sugerencia 2", "sugerencia 3"],
            "alertas": ["alerta si hay algo crítico"]
        }}
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
    
    def predict_future_expenses(self, usuario_id: int, meses_futuros: int = 3, datos_reales: Optional[Dict] = None, tiene_datos: bool = False) -> Dict[str, Any]:
        """
        Predecir gastos futuros basado en datos históricos reales
        """
        if not tiene_datos or not datos_reales:
            return {
                "status": "prediction_completed",
                "prediccion": {
                    "predicciones": [],
                    "tendencia_general": "Datos insuficientes para realizar predicciones. Necesitas al menos 30 días de historial.",
                    "factores_considerados": []
                },
                "meses_futuros": meses_futuros
            }
        
        datos_json = json.dumps(datos_reales, indent=2)
        
        prompt = f"""
        Predice los gastos futuros del usuario {usuario_id} para los próximos {meses_futuros} meses.
        
        DATOS HISTÓRICOS REALES:
        {datos_json}
        
        Basándote en:
        - Promedio mensual real de gastos
        - Distribución real por categorías
        - Patrones identificados en los datos
        - Estacionalidad (considera que estamos en noviembre)
        
        IMPORTANTE: Responde SOLO con un objeto JSON válido, sin formato markdown, sin bloques de código, sin ```json ni ```. Solo el JSON puro.
        
        Formato JSON requerido:
        {{
            "predicciones": [
                {{"mes": 1, "gasto_estimado": valor_basado_en_datos_reales, "confianza": "alta/media/baja"}},
                {{"mes": 2, "gasto_estimado": valor_basado_en_datos_reales, "confianza": "alta/media/baja"}},
                {{"mes": 3, "gasto_estimado": valor_basado_en_datos_reales, "confianza": "alta/media/baja"}}
            ],
            "tendencia_general": "descripción basada en datos reales",
            "factores_considerados": ["factor 1 del análisis de datos reales", "factor 2"]
        }}
        """
        
        response = self.generate_with_ai(prompt, temperature=0.3)
        
        try:
            prediccion = json.loads(response)
        except:
            # Fallback con predicción básica basada en promedio real
            promedio = datos_reales.get("promedio_mensual", 0)
            prediccion = {
                "predicciones": [
                    {"mes": i+1, "gasto_estimado": round(promedio * (1 + i*0.05), 2), "confianza": "baja"}
                    for i in range(meses_futuros)
                ],
                "tendencia_general": f"Proyección basada en promedio mensual de ${promedio:.2f}",
                "factores_considerados": ["Promedio histórico simple"]
            }
        
        return {
            "status": "prediction_completed",
            "prediccion": prediccion,
            "meses_futuros": meses_futuros
        }
