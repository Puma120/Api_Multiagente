"""
A2A Protocol (Agent-to-Agent)
Protocolo de comunicación general entre cualquier par de agentes
"""

from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class A2AProtocol:
    """
    Implementación del protocolo A2A para comunicación general entre agentes
    
    Características:
    - Comunicación directa y simple entre agentes
    - Mensajes sin estructura rígida
    - Ideal para notificaciones y coordinación básica
    """
    
    @staticmethod
    def create_message(
        sender: str,
        receiver: str,
        message_type: str,
        content: Dict[str, Any],
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """
        Crear mensaje A2A
        
        Args:
            sender: Nombre del agente emisor
            receiver: Nombre del agente receptor
            message_type: Tipo de mensaje (notificacion, solicitud, respuesta, etc.)
            content: Contenido del mensaje
            priority: Prioridad (low, normal, high)
        
        Returns:
            Mensaje formateado según protocolo A2A
        """
        return {
            "protocol": "A2A",
            "version": "1.0",
            "message_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "message_type": message_type,
            "priority": priority,
            "content": content
        }
    
    @staticmethod
    def validate_message(message: Dict[str, Any]) -> bool:
        """
        Validar que el mensaje cumple con el protocolo A2A
        """
        required_fields = [
            "protocol", "message_id", "timestamp", 
            "sender", "receiver", "message_type", "content"
        ]
        
        if not all(field in message for field in required_fields):
            return False
        
        if message["protocol"] != "A2A":
            return False
        
        return True
    
    @staticmethod
    def create_notification(
        sender: str,
        receiver: str,
        notification_type: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Crear notificación A2A
        """
        return A2AProtocol.create_message(
            sender=sender,
            receiver=receiver,
            message_type="notification",
            content={
                "notification_type": notification_type,
                "data": data
            }
        )
    
    @staticmethod
    def create_request(
        sender: str,
        receiver: str,
        action: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Crear solicitud A2A
        """
        return A2AProtocol.create_message(
            sender=sender,
            receiver=receiver,
            message_type="request",
            content={
                "action": action,
                "parameters": parameters
            }
        )
    
    @staticmethod
    def create_response(
        sender: str,
        receiver: str,
        request_id: str,
        status: str,
        result: Any
    ) -> Dict[str, Any]:
        """
        Crear respuesta A2A
        """
        return A2AProtocol.create_message(
            sender=sender,
            receiver=receiver,
            message_type="response",
            content={
                "request_id": request_id,
                "status": status,
                "result": result
            }
        )
