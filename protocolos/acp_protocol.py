"""
ACP Protocol (Agent Communication Protocol)
Protocolo de comunicación estructurada para intercambio de mensajes y diálogos
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

class ACPProtocol:
    """
    Implementación del protocolo ACP para comunicación estructurada
    
    Características:
    - Mensajes con estructura formal
    - Soporte para diálogos multi-turno
    - Ideal para intercambio de información compleja
    """
    
    PERFORMATIVES = [
        "inform",      # Informar un hecho
        "request",     # Solicitar acción
        "query",       # Consultar información
        "confirm",     # Confirmar información
        "refuse",      # Rechazar solicitud
        "propose",     # Proponer acción
        "accept",      # Aceptar propuesta
        "reject"       # Rechazar propuesta
    ]
    
    @staticmethod
    def create_message(
        sender: str,
        receiver: str,
        performative: str,
        content: Dict[str, Any],
        conversation_id: Optional[str] = None,
        reply_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crear mensaje ACP estructurado
        
        Args:
            sender: Agente emisor
            receiver: Agente receptor
            performative: Tipo de acto comunicativo
            content: Contenido del mensaje
            conversation_id: ID de conversación (para diálogos)
            reply_to: ID del mensaje al que responde
        
        Returns:
            Mensaje formateado según protocolo ACP
        """
        if performative not in ACPProtocol.PERFORMATIVES:
            raise ValueError(f"Performative inválido: {performative}")
        
        message_id = str(uuid.uuid4())
        
        return {
            "protocol": "ACP",
            "version": "1.0",
            "message_id": message_id,
            "conversation_id": conversation_id or message_id,
            "reply_to": reply_to,
            "timestamp": datetime.utcnow().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "performative": performative,
            "content": content,
            "language": "es-MX"
        }
    
    @staticmethod
    def validate_message(message: Dict[str, Any]) -> bool:
        """
        Validar mensaje ACP
        """
        required_fields = [
            "protocol", "message_id", "conversation_id",
            "timestamp", "sender", "receiver", 
            "performative", "content"
        ]
        
        if not all(field in message for field in required_fields):
            return False
        
        if message["protocol"] != "ACP":
            return False
        
        if message["performative"] not in ACPProtocol.PERFORMATIVES:
            return False
        
        return True
    
    @staticmethod
    def inform(sender: str, receiver: str, fact: Dict[str, Any], 
               conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Crear mensaje de tipo INFORM (informar un hecho)
        """
        return ACPProtocol.create_message(
            sender=sender,
            receiver=receiver,
            performative="inform",
            content={"fact": fact},
            conversation_id=conversation_id
        )
    
    @staticmethod
    def request(sender: str, receiver: str, action: str, 
                parameters: Dict[str, Any],
                conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Crear mensaje de tipo REQUEST (solicitar acción)
        """
        return ACPProtocol.create_message(
            sender=sender,
            receiver=receiver,
            performative="request",
            content={
                "action": action,
                "parameters": parameters
            },
            conversation_id=conversation_id
        )
    
    @staticmethod
    def query(sender: str, receiver: str, query_type: str,
              conditions: Dict[str, Any],
              conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Crear mensaje de tipo QUERY (consultar información)
        """
        return ACPProtocol.create_message(
            sender=sender,
            receiver=receiver,
            performative="query",
            content={
                "query_type": query_type,
                "conditions": conditions
            },
            conversation_id=conversation_id
        )
    
    @staticmethod
    def confirm(sender: str, receiver: str, fact: Dict[str, Any],
                reply_to: str,
                conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Crear mensaje de tipo CONFIRM (confirmar información)
        """
        return ACPProtocol.create_message(
            sender=sender,
            receiver=receiver,
            performative="confirm",
            content={"confirmed": fact},
            conversation_id=conversation_id,
            reply_to=reply_to
        )
    
    @staticmethod
    def propose(sender: str, receiver: str, proposal: Dict[str, Any],
                conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Crear mensaje de tipo PROPOSE (proponer acción)
        """
        return ACPProtocol.create_message(
            sender=sender,
            receiver=receiver,
            performative="propose",
            content={"proposal": proposal},
            conversation_id=conversation_id
        )
