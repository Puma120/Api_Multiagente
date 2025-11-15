import google.generativeai as genai
from datetime import datetime
from typing import Dict, Any, Optional, List
import json
import logging
from config import GOOGLE_API_KEY

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar Google AI
genai.configure(api_key=GOOGLE_API_KEY)

class BaseAgent:
    """
    Clase base para todos los agentes del sistema multiagente
    """
    
    def __init__(self, name: str, model_name: str, role: str):
        self.name = name
        self.model_name = model_name
        self.role = role
        self.model = genai.GenerativeModel(model_name)
        self.message_history = []
        logger.info(f"✅ Agente {self.name} iniciado con modelo {self.model_name}")
    
    def log_message(self, protocol: str, message_type: str, content: Dict[str, Any]):
        """
        Registrar mensaje en el historial del agente
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "protocol": protocol,
            "message_type": message_type,
            "content": content
        }
        self.message_history.append(log_entry)
        logger.info(f"[{self.name}] {protocol} - {message_type}: {json.dumps(content)[:100]}")
    
    def send_message(self, to_agent: str, protocol: str, message_type: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enviar mensaje a otro agente usando un protocolo específico
        """
        message = {
            "from": self.name,
            "to": to_agent,
            "protocol": protocol,
            "type": message_type,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.log_message(protocol, f"SEND-{message_type}", content)
        try:
            # Delivery via message bus to ensure inter-agent collaboration
            from agentes import message_bus
            response = message_bus.deliver(message)
            return response
        except Exception:
            # Fallback: return the message if bus not available
            return message
    
    def receive_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Recibir y procesar mensaje de otro agente
        """
        self.log_message(message["protocol"], f"RECEIVE-{message['type']}", message["content"])
        return self.process_message(message)
    
    def process_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Procesar mensaje recibido (debe ser implementado por cada agente específico)
        """
        raise NotImplementedError("Cada agente debe implementar process_message")
    
    def generate_with_ai(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generar respuesta usando el modelo Gemini asignado
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                )
            )
            # Limpiar formato markdown de la respuesta
            text = response.text.strip()
            
            # Remover bloques de código markdown si existen
            if text.startswith("```json"):
                text = text[7:]  # Remover ```json
            elif text.startswith("```"):
                text = text[3:]  # Remover ```
            
            if text.endswith("```"):
                text = text[:-3]  # Remover ```
            
            return text.strip()
        except Exception as e:
            logger.error(f"Error al generar con IA: {str(e)}")
            return "{}"
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Obtener historial de mensajes del agente
        """
        return self.message_history
    
    def clear_history(self):
        """
        Limpiar historial de mensajes
        """
        self.message_history = []
        logger.info(f"🗑️ Historial de {self.name} limpiado")
