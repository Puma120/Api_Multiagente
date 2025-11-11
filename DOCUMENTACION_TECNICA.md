# 📊 Documentación Técnica - Flujos y Protocolos

## Tabla de Contenidos
1. [Flujos de Comunicación Detallados](#flujos-de-comunicación-detallados)
2. [Especificación de Protocolos](#especificación-de-protocolos)
3. [Casos de Uso](#casos-de-uso)
4. [Ejemplos de Mensajes](#ejemplos-de-mensajes)

## Flujos de Comunicación Detallados

### Flujo 1: Creación de Transacción con Verificación de Presupuesto

**Objetivo**: Registrar una transacción y verificar si se debe generar alerta de presupuesto

**Participantes**: FastAPI → Base de Datos → Ejecutor → Notificador → Interfaz

**Protocolo Principal**: A2A (Agent-to-Agent)

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────┐
│ Usuario │────▶│ FastAPI  │────▶│ Database │────▶│  Ejecutor   │────▶│Notificador│
└─────────┘     └──────────┘     └──────────┘     └─────────────┘     └──────────┘
                                                           │                   │
                                                           │                   ▼
                                                           │            ┌──────────┐
                                                           └───────────▶│ Interfaz │
                                                                        └──────────┘
```

**Pasos**:
1. Usuario envía POST /transacciones
2. FastAPI valida datos con Pydantic
3. Se guarda en PostgreSQL
4. Si es gasto, se verifica presupuesto
5. Si gastado >= 80% límite:
   - Ejecutor crea mensaje A2A
   - Notificador genera alerta
   - Interfaz formatea con AGUI
6. Respuesta al usuario

**Código del Mensaje A2A**:
```python
{
    "protocol": "A2A",
    "message_id": "a2a-123e4567-e89b",
    "timestamp": "2025-11-10T10:30:00Z",
    "sender": "Ejecutor",
    "receiver": "Notificador",
    "message_type": "notification",
    "priority": "high",
    "content": {
        "notification_type": "budget_alert",
        "data": {
            "usuario_id": 1,
            "categoria": "alimentacion",
            "porcentaje": 85.0,
            "gastado": 4250.0,
            "limite": 5000.0
        }
    }
}
```

---

### Flujo 2: Análisis Financiero Completo (Coordinado)

**Objetivo**: Realizar análisis completo coordinando múltiples agentes

**Participantes**: Planificador → Ejecutor + Knowledge Base + Notificador → Interfaz

**Protocolo Principal**: ANP (Agent Negotiation Protocol)

```
┌─────────┐     ┌─────────────┐
│ Usuario │────▶│Planificador │
└─────────┘     └──────┬──────┘
                       │ ANP: Task Distribution
                ┌──────┴──────┬──────────────┐
                │             │              │
                ▼             ▼              ▼
         ┌──────────┐  ┌──────────┐  ┌────────────┐
         │Ejecutor  │  │Knowledge │  │Notificador │
         │  (ACP)   │  │Base(MCP) │  │   (A2A)    │
         └────┬─────┘  └────┬─────┘  └─────┬──────┘
              │             │              │
              └─────────────┴──────────────┘
                            │
                            ▼
                     ┌──────────┐
                     │ Interfaz │
                     │  (AGUI)  │
                     └──────────┘
```

**Negociación ANP**:
```python
{
    "protocol": "ANP",
    "negotiation_id": "anp-789abc-def012",
    "timestamp": "2025-11-10T10:35:00Z",
    "initiator": "Planificador",
    "participants": ["Ejecutor", "KnowledgeBase", "Notificador"],
    "negotiation_type": "task_allocation",
    "status": "proposed",
    "subject": {
        "description": "Análisis financiero completo del usuario",
        "total_tasks": 3
    },
    "terms": {
        "tasks": [
            {
                "id": 1,
                "tipo": "calcular_balance",
                "agente": "Ejecutor",
                "prioridad": "alta",
                "protocolo": "ACP"
            },
            {
                "id": 2,
                "tipo": "consultar_historico",
                "agente": "KnowledgeBase",
                "prioridad": "media",
                "protocolo": "MCP"
            },
            {
                "id": 3,
                "tipo": "generar_alertas",
                "agente": "Notificador",
                "prioridad": "media",
                "protocolo": "A2A"
            }
        ],
        "distribution_strategy": "balanced",
        "priority_order": "sequential"
    }
}
```

---

### Flujo 3: Consulta de Datos Históricos con Análisis

**Objetivo**: Obtener datos históricos, analizarlos y generar recomendaciones

**Participantes**: Knowledge Base → Ejecutor → Interfaz

**Protocolo Principal**: MCP (Message Content Protocol)

```
┌─────────┐     ┌──────────────┐     ┌──────────┐
│ FastAPI │────▶│Knowledge Base│────▶│ Database │
└─────────┘     └──────┬───────┘     └──────────┘
                       │ MCP: Query Result
                       ▼
                ┌──────────┐
                │Ejecutor  │
                │  (ACP)   │
                └────┬─────┘
                     │ AGUI: Formatted Data
                     ▼
              ┌──────────┐
              │ Interfaz │
              └──────────┘
```

**Mensaje MCP**:
```python
{
    "protocol": "MCP",
    "version": "1.0",
    "message_id": "mcp-456def-789ghi",
    "timestamp": "2025-11-10T10:40:00Z",
    "sender": "KnowledgeBase",
    "content_type": "query_result",
    "schema_version": "1.0",
    "data": {
        "query_type": "transactions",
        "results": [
            {
                "id": 1,
                "type": "gasto",
                "amount": 1500.0,
                "category": "alimentacion",
                "date": "2025-11-05"
            }
        ],
        "total_count": 45,
        "filters": {
            "usuario_id": 1,
            "periodo_dias": 30
        },
        "retrieved_at": "2025-11-10T10:40:00Z"
    },
    "metadata": {},
    "validation": {
        "validated": true,
        "validation_timestamp": "2025-11-10T10:40:00Z"
    }
}
```

---

## Especificación de Protocolos

### A2A (Agent-to-Agent)

**Características**:
- Comunicación simple y directa
- Sin estructura rígida
- Ideal para notificaciones

**Estructura del Mensaje**:
```python
{
    "protocol": "A2A",
    "version": "1.0",
    "message_id": "uuid",
    "timestamp": "ISO8601",
    "sender": "nombre_agente",
    "receiver": "nombre_agente",
    "message_type": "notification|request|response",
    "priority": "low|normal|high",
    "content": {}
}
```

**Casos de Uso**:
- Notificaciones simples
- Coordinación básica
- Alertas urgentes

---

### ACP (Agent Communication Protocol)

**Características**:
- Mensajes con estructura formal
- Soporte para diálogos multi-turno
- Performatives estándar (FIPA)

**Performatives**:
- `inform`: Informar un hecho
- `request`: Solicitar acción
- `query`: Consultar información
- `confirm`: Confirmar información
- `refuse`: Rechazar solicitud
- `propose`: Proponer acción
- `accept`: Aceptar propuesta
- `reject`: Rechazar propuesta

**Estructura del Mensaje**:
```python
{
    "protocol": "ACP",
    "version": "1.0",
    "message_id": "uuid",
    "conversation_id": "uuid",
    "reply_to": "uuid|null",
    "timestamp": "ISO8601",
    "sender": "nombre_agente",
    "receiver": "nombre_agente",
    "performative": "inform|request|query|...",
    "content": {},
    "language": "es-MX"
}
```

**Ejemplo de Diálogo**:
```python
# Mensaje 1: REQUEST
{
    "performative": "request",
    "conversation_id": "conv-123",
    "content": {
        "action": "calcular_balance",
        "parameters": {"usuario_id": 1}
    }
}

# Mensaje 2: CONFIRM (respuesta)
{
    "performative": "confirm",
    "conversation_id": "conv-123",
    "reply_to": "msg-1",
    "content": {
        "confirmed": {"balance": 15000.0}
    }
}
```

---

### ANP (Agent Negotiation Protocol)

**Características**:
- Negociación de recursos y tareas
- Resolución de conflictos
- Múltiples rondas de negociación

**Tipos de Negociación**:
- `task_allocation`: Asignación de tareas
- `resource_sharing`: Compartir recursos
- `conflict_resolution`: Resolver conflictos
- `priority_negotiation`: Negociar prioridades

**Estados**:
- `proposed`: Propuesta inicial
- `accepted`: Aceptada
- `rejected`: Rechazada
- `counter`: Contra-propuesta
- `committed`: Comprometida

**Estructura de Negociación**:
```python
{
    "protocol": "ANP",
    "version": "1.0",
    "negotiation_id": "uuid",
    "timestamp": "ISO8601",
    "initiator": "nombre_agente",
    "participants": ["agente1", "agente2"],
    "negotiation_type": "task_allocation|...",
    "status": "proposed|accepted|...",
    "subject": {},
    "terms": {},
    "deadline": "ISO8601|null",
    "rounds": []
}
```

---

### AGUI (Agent-to-User Interface)

**Características**:
- Optimizado para presentación visual
- Componentes UI predefinidos
- Acciones interactivas

**Componentes UI**:
- `alert`: Alerta/Notificación
- `dashboard`: Panel de control
- `chart`: Gráfico
- `table`: Tabla de datos
- `form`: Formulario
- `card`: Tarjeta
- `list`: Lista
- `progress`: Barra de progreso

**Tipos de Acción**:
- `display`: Mostrar información
- `update`: Actualizar información
- `request_input`: Solicitar entrada
- `confirm`: Solicitar confirmación
- `navigate`: Navegar a otra vista

**Estructura del Mensaje**:
```python
{
    "protocol": "AGUI",
    "version": "1.0",
    "message_id": "uuid",
    "timestamp": "ISO8601",
    "agent": "nombre_agente",
    "user_id": 1,
    "action_type": "display|update|...",
    "component": "alert|dashboard|...",
    "priority": "low|normal|high",
    "data": {},
    "metadata": {
        "generated_by": "nombre_agente",
        "requires_interaction": boolean
    }
}
```

---

### MCP (Message Content Protocol)

**Características**:
- Formato estandarizado de contenido
- Validación de esquemas
- Semántica clara

**Tipos de Contenido**:
- `financial_data`: Datos financieros
- `transaction`: Transacción
- `budget`: Presupuesto
- `analysis`: Análisis
- `recommendation`: Recomendación
- `alert`: Alerta
- `query_result`: Resultado de consulta
- `status_update`: Actualización de estado

**Esquemas de Validación**:
```python
DATA_SCHEMAS = {
    "transaction": {
        "required": ["id", "type", "amount", "date"],
        "optional": ["category", "description", "user_id"]
    },
    "budget": {
        "required": ["category", "limit", "period"],
        "optional": ["spent", "remaining", "alerts"]
    }
}
```

---

## Casos de Uso

### Caso 1: Alerta de Presupuesto Excedido
**Protocolos**: A2A + AGUI

```
1. Usuario gasta $4500 (90% del presupuesto de $5000)
2. Ejecutor detecta exceso
3. A2A: Ejecutor → Notificador
4. Notificador genera alerta con IA
5. AGUI: Notificador → Interfaz
6. Interfaz formatea para UI
7. Frontend muestra alerta visual
```

### Caso 2: Análisis Predictivo de Gastos
**Protocolos**: ANP + MCP + ACP

```
1. Usuario solicita predicción de gastos
2. ANP: Planificador distribuye tareas
3. MCP: Knowledge Base consulta histórico
4. ACP: Ejecutor analiza con IA
5. ACP: Knowledge Base almacena predicción
6. AGUI: Interfaz presenta resultados
```

### Caso 3: Recomendación de Ahorro Personalizada
**Protocolos**: MCP + A2A + AGUI

```
1. Usuario solicita recomendaciones
2. MCP: Knowledge Base analiza patrones
3. A2A: Ejecutor procesa con IA
4. A2A: Notificador genera mensaje motivacional
5. AGUI: Interfaz presenta recomendaciones
```

---

## Ejemplos de Mensajes Completos

### Ejemplo 1: Alerta de Presupuesto (A2A)
```json
{
    "protocol": "A2A",
    "version": "1.0",
    "message_id": "a2a-abc123",
    "timestamp": "2025-11-10T14:30:00Z",
    "sender": "Ejecutor",
    "receiver": "Notificador",
    "message_type": "notification",
    "priority": "high",
    "content": {
        "notification_type": "budget_alert",
        "data": {
            "usuario_id": 1,
            "categoria": "alimentacion",
            "porcentaje": 90.0,
            "gastado": 4500.0,
            "limite": 5000.0,
            "mensaje": "Has gastado el 90% de tu presupuesto de alimentación"
        }
    }
}
```

### Ejemplo 2: Consulta de Transacciones (ACP)
```json
{
    "protocol": "ACP",
    "version": "1.0",
    "message_id": "acp-def456",
    "conversation_id": "conv-789",
    "reply_to": null,
    "timestamp": "2025-11-10T14:35:00Z",
    "sender": "Ejecutor",
    "receiver": "KnowledgeBase",
    "performative": "query",
    "content": {
        "query_type": "transactions",
        "conditions": {
            "usuario_id": 1,
            "periodo_dias": 30,
            "tipo": "gasto"
        }
    },
    "language": "es-MX"
}
```

### Ejemplo 3: Dashboard UI (AGUI)
```json
{
    "protocol": "AGUI",
    "version": "1.0",
    "message_id": "agui-ghi789",
    "timestamp": "2025-11-10T14:40:00Z",
    "agent": "Interfaz",
    "user_id": 1,
    "action_type": "display",
    "component": "dashboard",
    "priority": "normal",
    "data": {
        "sections": [
            {
                "type": "summary",
                "title": "Resumen Financiero",
                "data": {
                    "balance": 15000.0,
                    "ingresos_mes": 50000.0,
                    "gastos_mes": 35000.0
                }
            },
            {
                "type": "chart",
                "title": "Gastos por Categoría",
                "chart_type": "pie",
                "data": {
                    "alimentacion": 4500,
                    "transporte": 2800,
                    "entretenimiento": 1500
                }
            }
        ],
        "refresh_interval": 30,
        "last_updated": "2025-11-10T14:40:00Z"
    },
    "metadata": {
        "generated_by": "Interfaz",
        "requires_interaction": false
    }
}
```

---

## Resumen de Mapeo Protocolo-Agente

| Agente | Protocolo Primario | Protocolo Secundario | Casos de Uso |
|--------|-------------------|---------------------|--------------|
| Planificador | ANP | A2A | Distribución de tareas, coordinación |
| Ejecutor | ACP | A2A | Cálculos, consultas estructuradas |
| Notificador | A2A | AGUI | Alertas, notificaciones |
| Interfaz | AGUI | A2A | Presentación visual |
| Knowledge Base | MCP | ACP | Almacenamiento, consultas validadas |
| Monitor | A2A | ANP | Supervisión, salud del sistema |

---

**Nota**: Todos los protocolos incluyen validación de mensajes para garantizar la correcta comunicación entre agentes.
