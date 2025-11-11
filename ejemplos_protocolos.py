"""
Ejemplos de uso de los protocolos del sistema multiagente
"""

# ============================================================
# EJEMPLO 1: Protocolo A2A (Agent-to-Agent)
# ============================================================

from protocolos.a2a_protocol import A2AProtocol

# Crear notificación simple
mensaje_a2a = A2AProtocol.create_notification(
    sender="Ejecutor",
    receiver="Notificador",
    notification_type="budget_alert",
    data={
        "usuario_id": 1,
        "categoria": "alimentacion",
        "porcentaje": 85.0,
        "mensaje": "Has gastado el 85% de tu presupuesto"
    }
)

print("Mensaje A2A:", mensaje_a2a)

# ============================================================
# EJEMPLO 2: Protocolo ACP (Agent Communication Protocol)
# ============================================================

from protocolos.acp_protocol import ACPProtocol

# Consultar transacciones
query_transacciones = ACPProtocol.query(
    sender="Ejecutor",
    receiver="KnowledgeBase",
    query_type="transactions",
    conditions={
        "usuario_id": 1,
        "periodo_dias": 30,
        "tipo": "gasto"
    }
)

print("Query ACP:", query_transacciones)

# Confirmar recepción de datos
confirmacion = ACPProtocol.confirm(
    sender="KnowledgeBase",
    receiver="Ejecutor",
    fact={"transacciones_encontradas": 45},
    reply_to=query_transacciones["message_id"]
)

print("Confirmación ACP:", confirmacion)

# ============================================================
# EJEMPLO 3: Protocolo ANP (Agent Negotiation Protocol)
# ============================================================

from protocolos.anp_protocol import ANPProtocol

# Negociar distribución de tareas
negociacion_tareas = ANPProtocol.allocate_tasks(
    planificador="Planificador",
    ejecutores=["Ejecutor", "KnowledgeBase", "Notificador"],
    tasks=[
        {
            "id": 1,
            "tipo": "calcular_balance",
            "descripcion": "Calcular balance financiero actual",
            "prioridad": "alta"
        },
        {
            "id": 2,
            "tipo": "analizar_historico",
            "descripcion": "Analizar patrones de los últimos 6 meses",
            "prioridad": "media"
        },
        {
            "id": 3,
            "tipo": "generar_alertas",
            "descripcion": "Generar alertas si hay desviaciones",
            "prioridad": "media"
        }
    ]
)

print("Negociación ANP:", negociacion_tareas)

# ============================================================
# EJEMPLO 4: Protocolo AGUI (Agent-to-User Interface)
# ============================================================

from protocolos.agui_protocol import AGUIProtocol

# Mostrar alerta en UI
alerta_ui = AGUIProtocol.display_alert(
    agent="Notificador",
    user_id=1,
    level="warning",
    title="Presupuesto Cerca del Límite",
    message="Has gastado el 85% de tu presupuesto de alimentación este mes.",
    actions=[
        {"label": "Ver Detalles", "action": "show_budget_details"},
        {"label": "Ignorar", "action": "dismiss"}
    ]
)

print("Alerta AGUI:", alerta_ui)

# Crear dashboard
dashboard = AGUIProtocol.display_dashboard(
    agent="Interfaz",
    user_id=1,
    sections=[
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
                "entretenimiento": 1500,
                "servicios": 3200
            }
        }
    ]
)

print("Dashboard AGUI:", dashboard)

# ============================================================
# EJEMPLO 5: Protocolo MCP (Message Content Protocol)
# ============================================================

from protocolos.mcp_protocol import MCPProtocol

# Crear transacción con validación
transaccion_mcp = MCPProtocol.create_transaction(
    sender="FastAPI",
    transaction_id=123,
    transaction_type="gasto",
    amount=1500.0,
    date="2025-11-10T10:30:00Z",
    category="alimentacion",
    description="Compra en supermercado"
)

# Validar mensaje
validacion = MCPProtocol.validate_message(transaccion_mcp)
print("Transacción MCP:", transaccion_mcp)
print("Validación:", validacion)

# Crear resultado de consulta
resultado_query = MCPProtocol.create_query_result(
    sender="KnowledgeBase",
    query_type="transactions",
    results=[
        {
            "id": 1,
            "type": "gasto",
            "amount": 1500.0,
            "category": "alimentacion",
            "date": "2025-11-10"
        },
        {
            "id": 2,
            "type": "gasto",
            "amount": 800.0,
            "category": "transporte",
            "date": "2025-11-09"
        }
    ],
    total_count=45,
    filters={"usuario_id": 1, "periodo_dias": 30}
)

print("Resultado Query MCP:", resultado_query)

# ============================================================
# EJEMPLO 6: Uso de Agentes
# ============================================================

from agentes import (
    PlanificadorAgent,
    EjecutorAgent,
    NotificadorAgent,
    InterfazAgent,
    KnowledgeBaseAgent
)

# Inicializar agentes
planificador = PlanificadorAgent()
ejecutor = EjecutorAgent()
notificador = NotificadorAgent()
interfaz = InterfazAgent()
knowledge_base = KnowledgeBaseAgent()

# FLUJO COMPLETO: Análisis Financiero
print("\n" + "="*60)
print("EJEMPLO DE FLUJO COMPLETO")
print("="*60)

# 1. Planificador crea plan
print("\n1. PLANIFICADOR: Creando plan de análisis...")
plan = planificador.create_financial_plan({
    "usuario_id": 1,
    "objetivo": "analizar_finanzas_mensuales"
})
print(f"Plan creado con {len(plan['plan']['subtareas'])} subtareas")

# 2. Ejecutor realiza cálculos
print("\n2. EJECUTOR: Calculando balance...")
balance = ejecutor.calculate_balance({
    "usuario_id": 1,
    "periodo_dias": 30
})
print(f"Balance calculado: {balance['status']}")

# 3. Notificador genera alerta si es necesario
print("\n3. NOTIFICADOR: Verificando condiciones de alerta...")
alerta = notificador.create_alert({
    "usuario_id": 1,
    "tipo": "presupuesto_cerca_limite",
    "datos": {
        "categoria": "alimentacion",
        "porcentaje": 85.0,
        "gastado": 4250.0,
        "limite": 5000.0
    }
})
print(f"Alerta generada: {alerta['alerta']['titulo']}")

# 4. Interfaz formatea para presentación
print("\n4. INTERFAZ: Formateando dashboard...")
dashboard_data = interfaz.create_dashboard({
    "usuario_id": 1,
    "datos": {
        "balance": balance,
        "alertas": [alerta]
    }
})
print(f"Dashboard creado: {dashboard_data['status']}")

# 5. Knowledge Base obtiene insights
print("\n5. KNOWLEDGE BASE: Generando insights...")
insights = knowledge_base.get_spending_insights(
    usuario_id=1,
    categoria="alimentacion"
)
print(f"Insights generados: {insights['status']}")

print("\n" + "="*60)
print("FLUJO COMPLETADO EXITOSAMENTE")
print("="*60)

# ============================================================
# EJEMPLO 7: Verificar Historial de Comunicación
# ============================================================

print("\n" + "="*60)
print("HISTORIAL DE COMUNICACIÓN")
print("="*60)

agentes = {
    "Planificador": planificador,
    "Ejecutor": ejecutor,
    "Notificador": notificador,
    "Interfaz": interfaz,
    "Knowledge Base": knowledge_base
}

for nombre, agente in agentes.items():
    historial = agente.get_history()
    print(f"\n{nombre}: {len(historial)} mensajes en historial")
    if historial:
        ultimo = historial[-1]
        print(f"  Último mensaje: {ultimo['message_type']} vía {ultimo['protocol']}")
