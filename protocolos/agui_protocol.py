"""
AGUI Protocol (Agent-to-User Interface)
Protocolo de comunicación entre agentes y la interfaz de usuario
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

class AGUIProtocol:
    """
    Implementación del protocolo AGUI para comunicación agente-interfaz
    
    Características:
    - Comunicación optimizada para presentación visual
    - Formato adaptado para consumo por frontend
    - Soporte para diferentes tipos de visualización
    """
    
    UI_COMPONENTS = [
        "alert",           # Alerta/Notificación
        "dashboard",       # Panel de control
        "chart",           # Gráfico
        "table",           # Tabla de datos
        "form",            # Formulario
        "card",            # Tarjeta de información
        "list",            # Lista
        "progress"         # Barra de progreso
    ]
    
    ACTION_TYPES = [
        "display",         # Mostrar información
        "update",          # Actualizar información
        "request_input",   # Solicitar entrada del usuario
        "confirm",         # Solicitar confirmación
        "navigate"         # Navegar a otra vista
    ]
    
    @staticmethod
    def create_ui_message(
        agent: str,
        action_type: str,
        component: str,
        data: Dict[str, Any],
        priority: str = "normal",
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Crear mensaje AGUI para la interfaz
        
        Args:
            agent: Nombre del agente emisor
            action_type: Tipo de acción (display, update, etc.)
            component: Componente UI a utilizar
            data: Datos a mostrar
            priority: Prioridad del mensaje
            user_id: ID del usuario destinatario
        
        Returns:
            Mensaje formateado según protocolo AGUI
        """
        if action_type not in AGUIProtocol.ACTION_TYPES:
            raise ValueError(f"Tipo de acción inválido: {action_type}")
        
        if component not in AGUIProtocol.UI_COMPONENTS:
            raise ValueError(f"Componente UI inválido: {component}")
        
        return {
            "protocol": "AGUI",
            "version": "1.0",
            "message_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent,
            "user_id": user_id,
            "action_type": action_type,
            "component": component,
            "priority": priority,
            "data": data,
            "metadata": {
                "generated_by": agent,
                "requires_interaction": action_type in ["request_input", "confirm"]
            }
        }
    
    @staticmethod
    def validate_message(message: Dict[str, Any]) -> bool:
        """
        Validar mensaje AGUI
        """
        required_fields = [
            "protocol", "message_id", "timestamp",
            "agent", "action_type", "component", "data"
        ]
        
        if not all(field in message for field in required_fields):
            return False
        
        if message["protocol"] != "AGUI":
            return False
        
        if message["action_type"] not in AGUIProtocol.ACTION_TYPES:
            return False
        
        if message["component"] not in AGUIProtocol.UI_COMPONENTS:
            return False
        
        return True
    
    @staticmethod
    def display_alert(
        agent: str,
        user_id: int,
        level: str,
        title: str,
        message: str,
        actions: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Crear mensaje para mostrar alerta
        """
        return AGUIProtocol.create_ui_message(
            agent=agent,
            action_type="display",
            component="alert",
            data={
                "level": level,
                "title": title,
                "message": message,
                "actions": actions or [],
                "dismissible": True
            },
            priority="high" if level == "critical" else "normal",
            user_id=user_id
        )
    
    @staticmethod
    def display_dashboard(
        agent: str,
        user_id: int,
        sections: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Crear mensaje para mostrar dashboard
        """
        return AGUIProtocol.create_ui_message(
            agent=agent,
            action_type="display",
            component="dashboard",
            data={
                "sections": sections,
                "refresh_interval": 30,  # segundos
                "last_updated": datetime.utcnow().isoformat()
            },
            user_id=user_id
        )
    
    @staticmethod
    def display_chart(
        agent: str,
        user_id: int,
        chart_type: str,
        title: str,
        data: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Crear mensaje para mostrar gráfico
        """
        return AGUIProtocol.create_ui_message(
            agent=agent,
            action_type="display",
            component="chart",
            data={
                "chart_type": chart_type,  # line, bar, pie, etc.
                "title": title,
                "data": data,
                "options": options or {}
            },
            user_id=user_id
        )
    
    @staticmethod
    def display_table(
        agent: str,
        user_id: int,
        title: str,
        columns: List[Dict[str, str]],
        rows: List[Dict[str, Any]],
        pagination: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """
        Crear mensaje para mostrar tabla
        """
        return AGUIProtocol.create_ui_message(
            agent=agent,
            action_type="display",
            component="table",
            data={
                "title": title,
                "columns": columns,
                "rows": rows,
                "pagination": pagination,
                "sortable": True,
                "filterable": True
            },
            user_id=user_id
        )
    
    @staticmethod
    def request_user_input(
        agent: str,
        user_id: int,
        form_fields: List[Dict[str, Any]],
        title: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Solicitar entrada del usuario
        """
        return AGUIProtocol.create_ui_message(
            agent=agent,
            action_type="request_input",
            component="form",
            data={
                "title": title,
                "description": description,
                "fields": form_fields,
                "submit_label": "Enviar",
                "cancel_label": "Cancelar"
            },
            priority="high",
            user_id=user_id
        )
    
    @staticmethod
    def update_component(
        agent: str,
        user_id: int,
        component: str,
        component_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Actualizar componente existente
        """
        return AGUIProtocol.create_ui_message(
            agent=agent,
            action_type="update",
            component=component,
            data={
                "component_id": component_id,
                "updates": updates,
                "animate": True
            },
            user_id=user_id
        )
