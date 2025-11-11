"""
MCP Protocol (Message Content Protocol)
Protocolo para definir la semántica del contenido del mensaje
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

class MCPProtocol:
    """
    Implementación del protocolo MCP para estandarizar contenido de mensajes
    
    Características:
    - Formato estandarizado de contenido
    - Semántica clara y consistente
    - Validación de tipos de datos
    """
    
    CONTENT_TYPES = [
        "financial_data",          # Datos financieros
        "transaction",             # Transacción
        "budget",                  # Presupuesto
        "analysis",                # Análisis
        "recommendation",          # Recomendación
        "alert",                   # Alerta
        "query_result",            # Resultado de consulta
        "status_update"            # Actualización de estado
    ]
    
    DATA_SCHEMAS = {
        "financial_data": {
            "required": ["amount", "currency", "date"],
            "optional": ["category", "description", "metadata"]
        },
        "transaction": {
            "required": ["id", "type", "amount", "date"],
            "optional": ["category", "description", "user_id"]
        },
        "budget": {
            "required": ["category", "limit", "period"],
            "optional": ["spent", "remaining", "alerts"]
        },
        "analysis": {
            "required": ["type", "period", "results"],
            "optional": ["recommendations", "visualizations"]
        }
    }
    
    @staticmethod
    def create_message(
        sender: str,
        content_type: str,
        data: Dict[str, Any],
        schema_version: str = "1.0",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Crear mensaje MCP con contenido estandarizado
        
        Args:
            sender: Agente emisor
            content_type: Tipo de contenido
            data: Datos del mensaje
            schema_version: Versión del esquema
            metadata: Metadatos adicionales
        
        Returns:
            Mensaje formateado según protocolo MCP
        """
        if content_type not in MCPProtocol.CONTENT_TYPES:
            raise ValueError(f"Tipo de contenido inválido: {content_type}")
        
        message_id = str(uuid.uuid4())
        
        return {
            "protocol": "MCP",
            "version": "1.0",
            "message_id": message_id,
            "timestamp": datetime.utcnow().isoformat(),
            "sender": sender,
            "content_type": content_type,
            "schema_version": schema_version,
            "data": data,
            "metadata": metadata or {},
            "validation": {
                "validated": True,
                "validation_timestamp": datetime.utcnow().isoformat()
            }
        }
    
    @staticmethod
    def validate_message(message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validar mensaje MCP
        
        Returns:
            Dict con resultado de validación
        """
        errors = []
        
        # Validar campos requeridos del protocolo
        required_protocol_fields = [
            "protocol", "message_id", "timestamp",
            "sender", "content_type", "data"
        ]
        
        for field in required_protocol_fields:
            if field not in message:
                errors.append(f"Campo requerido faltante: {field}")
        
        if errors:
            return {
                "valid": False,
                "errors": errors
            }
        
        # Validar protocolo
        if message["protocol"] != "MCP":
            errors.append(f"Protocolo incorrecto: {message['protocol']}")
        
        # Validar tipo de contenido
        content_type = message.get("content_type")
        if content_type not in MCPProtocol.CONTENT_TYPES:
            errors.append(f"Tipo de contenido inválido: {content_type}")
        
        # Validar esquema de datos si está definido
        if content_type in MCPProtocol.DATA_SCHEMAS and not errors:
            schema = MCPProtocol.DATA_SCHEMAS[content_type]
            data = message.get("data", {})
            
            # Validar campos requeridos del esquema
            for field in schema.get("required", []):
                if field not in data:
                    errors.append(f"Campo de datos requerido faltante: {field}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors if errors else None
        }
    
    @staticmethod
    def create_financial_data(
        sender: str,
        amount: float,
        currency: str,
        date: str,
        category: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crear mensaje con datos financieros
        """
        return MCPProtocol.create_message(
            sender=sender,
            content_type="financial_data",
            data={
                "amount": amount,
                "currency": currency,
                "date": date,
                "category": category,
                "description": description
            }
        )
    
    @staticmethod
    def create_transaction(
        sender: str,
        transaction_id: int,
        transaction_type: str,
        amount: float,
        date: str,
        category: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crear mensaje con transacción
        """
        return MCPProtocol.create_message(
            sender=sender,
            content_type="transaction",
            data={
                "id": transaction_id,
                "type": transaction_type,
                "amount": amount,
                "date": date,
                "category": category,
                "description": description
            }
        )
    
    @staticmethod
    def create_budget(
        sender: str,
        category: str,
        limit: float,
        period: Dict[str, Any],
        spent: Optional[float] = None,
        remaining: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Crear mensaje con presupuesto
        """
        return MCPProtocol.create_message(
            sender=sender,
            content_type="budget",
            data={
                "category": category,
                "limit": limit,
                "period": period,
                "spent": spent or 0.0,
                "remaining": remaining or limit
            }
        )
    
    @staticmethod
    def create_analysis(
        sender: str,
        analysis_type: str,
        period: Dict[str, str],
        results: Dict[str, Any],
        recommendations: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Crear mensaje con análisis
        """
        return MCPProtocol.create_message(
            sender=sender,
            content_type="analysis",
            data={
                "type": analysis_type,
                "period": period,
                "results": results,
                "recommendations": recommendations or []
            }
        )
    
    @staticmethod
    def create_query_result(
        sender: str,
        query_type: str,
        results: List[Dict[str, Any]],
        total_count: int,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Crear mensaje con resultado de consulta
        """
        return MCPProtocol.create_message(
            sender=sender,
            content_type="query_result",
            data={
                "query_type": query_type,
                "results": results,
                "total_count": total_count,
                "filters": filters or {},
                "retrieved_at": datetime.utcnow().isoformat()
            }
        )
