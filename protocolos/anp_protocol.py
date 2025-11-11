"""
ANP Protocol (Agent Negotiation Protocol)
Protocolo de negociación para resolver conflictos y distribuir recursos/tareas
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

class ANPProtocol:
    """
    Implementación del protocolo ANP para negociación entre agentes
    
    Características:
    - Negociación de recursos y tareas
    - Resolución de conflictos
    - Distribución óptima de carga
    """
    
    NEGOTIATION_TYPES = [
        "task_allocation",      # Asignación de tareas
        "resource_sharing",     # Compartir recursos
        "conflict_resolution",  # Resolver conflictos
        "priority_negotiation"  # Negociar prioridades
    ]
    
    NEGOTIATION_STATUS = [
        "proposed",    # Propuesta inicial
        "accepted",    # Aceptada
        "rejected",    # Rechazada
        "counter",     # Contra-propuesta
        "committed"    # Comprometida
    ]
    
    @staticmethod
    def create_negotiation(
        initiator: str,
        participants: List[str],
        negotiation_type: str,
        subject: Dict[str, Any],
        terms: Dict[str, Any],
        deadline: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Iniciar negociación ANP
        
        Args:
            initiator: Agente que inicia la negociación
            participants: Lista de agentes participantes
            negotiation_type: Tipo de negociación
            subject: Tema de negociación
            terms: Términos de la negociación
            deadline: Fecha límite para respuesta
        
        Returns:
            Negociación formateada según protocolo ANP
        """
        if negotiation_type not in ANPProtocol.NEGOTIATION_TYPES:
            raise ValueError(f"Tipo de negociación inválido: {negotiation_type}")
        
        negotiation_id = str(uuid.uuid4())
        
        return {
            "protocol": "ANP",
            "version": "1.0",
            "negotiation_id": negotiation_id,
            "timestamp": datetime.utcnow().isoformat(),
            "initiator": initiator,
            "participants": participants,
            "negotiation_type": negotiation_type,
            "status": "proposed",
            "subject": subject,
            "terms": terms,
            "deadline": deadline,
            "rounds": []
        }
    
    @staticmethod
    def add_response(
        negotiation: Dict[str, Any],
        responder: str,
        status: str,
        response: Dict[str, Any],
        counter_terms: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Agregar respuesta a una negociación
        """
        if status not in ANPProtocol.NEGOTIATION_STATUS:
            raise ValueError(f"Estado inválido: {status}")
        
        round_entry = {
            "round_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "responder": responder,
            "status": status,
            "response": response,
            "counter_terms": counter_terms
        }
        
        negotiation["rounds"].append(round_entry)
        negotiation["status"] = status
        
        return negotiation
    
    @staticmethod
    def validate_negotiation(negotiation: Dict[str, Any]) -> bool:
        """
        Validar negociación ANP
        """
        required_fields = [
            "protocol", "negotiation_id", "timestamp",
            "initiator", "participants", "negotiation_type",
            "status", "subject", "terms"
        ]
        
        if not all(field in negotiation for field in required_fields):
            return False
        
        if negotiation["protocol"] != "ANP":
            return False
        
        if negotiation["negotiation_type"] not in ANPProtocol.NEGOTIATION_TYPES:
            return False
        
        return True
    
    @staticmethod
    def allocate_tasks(
        planificador: str,
        ejecutores: List[str],
        tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Crear negociación para asignación de tareas
        """
        return ANPProtocol.create_negotiation(
            initiator=planificador,
            participants=ejecutores,
            negotiation_type="task_allocation",
            subject={
                "description": "Asignación de tareas financieras",
                "total_tasks": len(tasks)
            },
            terms={
                "tasks": tasks,
                "distribution_strategy": "balanced",
                "priority_order": "sequential"
            }
        )
    
    @staticmethod
    def resolve_conflict(
        mediator: str,
        conflicting_agents: List[str],
        conflict_description: str,
        proposed_solution: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Crear negociación para resolver conflicto
        """
        return ANPProtocol.create_negotiation(
            initiator=mediator,
            participants=conflicting_agents,
            negotiation_type="conflict_resolution",
            subject={
                "conflict": conflict_description,
                "agents_involved": conflicting_agents
            },
            terms={
                "proposed_solution": proposed_solution,
                "requires_consensus": True
            }
        )
    
    @staticmethod
    def negotiate_resources(
        requester: str,
        resource_holders: List[str],
        resource_type: str,
        amount_needed: float
    ) -> Dict[str, Any]:
        """
        Crear negociación para compartir recursos
        """
        return ANPProtocol.create_negotiation(
            initiator=requester,
            participants=resource_holders,
            negotiation_type="resource_sharing",
            subject={
                "resource_type": resource_type,
                "amount_needed": amount_needed
            },
            terms={
                "distribution": "fair_share",
                "return_policy": "not_required"
            }
        )
