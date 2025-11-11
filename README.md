# 🤖 Sistema Multiagente de Finanzas Personales Inteligentes

Sistema avanzado de gestión financiera personal que utiliza múltiples agentes de IA (Google Gemini) trabajando en colaboración mediante protocolos de comunicación estandarizados.

## 👥 Datos del Equipo

- **Proyecto**: Sistema Multiagente de Finanzas Personales
- **Tecnologías**: FastAPI, PostgreSQL, Google Gemini AI, SQLAlchemy
- **Fecha**: Noviembre 2025

## 📋 Introducción

Este sistema implementa un enfoque multiagente para la gestión de finanzas personales, donde cada agente cumple un rol específico y se comunica con otros mediante protocolos estandarizados. El sistema utiliza modelos de IA de Google Gemini para proporcionar análisis inteligente, recomendaciones personalizadas y alertas proactivas.

### Objetivos Principales

- ✅ Gestión automática y colaborativa de finanzas personales
- ✅ Análisis inteligente mediante IA (Google Gemini)
- ✅ Comunicación estructurada entre agentes usando protocolos definidos
- ✅ API REST completa para integración con frontend
- ✅ Almacenamiento persistente en PostgreSQL (Render)

## 🏗️ Arquitectura Multiagente y Protocolos

### Agentes del Sistema

| Agente | Rol | Modelo Gemini | Protocolo Principal |
|--------|-----|---------------|---------------------|
| **Planificador** | Descompone tareas financieras en subtareas | gemini-2.0-flash | ANP |
| **Ejecutor** | Realiza cálculos y operaciones financieras | gemini-2.5-flash | ACP |
| **Notificador** | Envía alertas y notificaciones | gemini-2.0-flash | A2A |
| **Interfaz** | Formatea información para el usuario | gemini-2.0-flash | AGUI |
| **Knowledge Base** | Almacena y proporciona datos históricos | gemini-2.5-pro | MCP |
| **Monitor** | Supervisa el sistema multiagente | gemini-2.0-flash | Múltiples |

### Protocolos Implementados

#### 1. **A2A (Agent-to-Agent)** 
- **Propósito**: Comunicación general entre cualquier par de agentes
- **Uso**: Notificaciones simples y coordinación básica
- **Ejemplo**: Notificador → Interfaz para mostrar alertas
- **Archivo**: `protocolos/a2a_protocol.py`

#### 2. **ACP (Agent Communication Protocol)**
- **Propósito**: Intercambio estructurado de mensajes y diálogos
- **Uso**: Consultas complejas y respuestas estructuradas
- **Ejemplo**: Ejecutor → Knowledge Base para obtener transacciones
- **Archivo**: `protocolos/acp_protocol.py`
- **Performatives**: inform, request, query, confirm, propose, accept, reject

#### 3. **ANP (Agent Negotiation Protocol)**
- **Propósito**: Resolución de conflictos y distribución de tareas/recursos
- **Uso**: Planificación y asignación de subtareas
- **Ejemplo**: Planificador distribuye análisis financiero entre múltiples agentes
- **Archivo**: `protocolos/anp_protocol.py`

#### 4. **AGUI (Agent-to-User Interface)**
- **Propósito**: Comunicación optimizada agente-interfaz
- **Uso**: Presentación de información al usuario final
- **Ejemplo**: Interfaz formatea dashboard para visualización
- **Archivo**: `protocolos/agui_protocol.py`
- **Componentes**: alert, dashboard, chart, table, form, card, list, progress

#### 5. **MCP (Message Content Protocol)**
- **Propósito**: Estandarización del contenido de mensajes
- **Uso**: Formato y validación de datos financieros
- **Ejemplo**: Knowledge Base retorna datos con esquema validado
- **Archivo**: `protocolos/mcp_protocol.py`

## 🔄 Flujos de Comunicación Principales

### Flujo 1: Análisis Financiero Completo
```
Usuario → FastAPI → Planificador (ANP)
                         ↓
           [Descompone en subtareas]
                         ↓
              ┌──────────┼──────────┐
              ↓          ↓          ↓
         Ejecutor    Knowledge   Notificador
          (ACP)       Base (MCP)    (A2A)
              ↓          ↓          ↓
              └──────────┼──────────┘
                         ↓
                   Interfaz (AGUI)
                         ↓
                      Usuario
```

**Protocolo ANP**: Planificador negocia distribución de tareas
- Subtarea 1: Ejecutor calcula balance
- Subtarea 2: Knowledge Base analiza patrones históricos
- Subtarea 3: Notificador genera alertas si hay desviaciones

### Flujo 2: Creación de Transacción con Alerta
```
Usuario → FastAPI → [Guarda en DB]
                         ↓
                   Ejecutor (ACP)
                         ↓
              [Verifica presupuesto]
                         ↓
                 ¿Excede 80%? → Sí → Notificador (A2A)
                                          ↓
                                    Interfaz (AGUI)
                                          ↓
                                       Usuario
```

**Protocolo A2A**: Comunicación simple para alertas
**Protocolo AGUI**: Formato visual para el usuario

### Flujo 3: Consulta de Datos Históricos
```
Usuario → FastAPI → Knowledge Base (MCP)
                         ↓
              [Consulta en PostgreSQL]
                         ↓
              [Valida con esquema MCP]
                         ↓
                 Ejecutor (ACP)
                         ↓
              [Genera análisis con IA]
                         ↓
                   Interfaz (AGUI)
                         ↓
                      Usuario
```

**Protocolo MCP**: Datos estandarizados y validados
**Protocolo ACP**: Intercambio estructurado para análisis

## 💻 Desarrollo de la Solución

### Estructura del Proyecto

```
Protocolos_tarea/
├── agentes/
│   ├── __init__.py
│   ├── base_agent.py              # Clase base para todos los agentes
│   ├── planificador_agent.py      # Agente Planificador (ANP)
│   ├── ejecutor_agent.py          # Agente Ejecutor (ACP)
│   ├── notificador_agent.py       # Agente Notificador (A2A)
│   ├── interfaz_agent.py          # Agente Interfaz (AGUI)
│   ├── knowledge_base_agent.py    # Agente Knowledge Base (MCP)
│   └── monitor_agent.py           # Agente Monitor
├── protocolos/
│   ├── __init__.py
│   ├── a2a_protocol.py            # Protocolo Agent-to-Agent
│   ├── acp_protocol.py            # Protocolo de Comunicación
│   ├── anp_protocol.py            # Protocolo de Negociación
│   ├── agui_protocol.py           # Protocolo Agent-UI
│   └── mcp_protocol.py            # Protocolo de Contenido
├── config.py                       # Configuración general
├── database.py                     # Conexión PostgreSQL
├── models.py                       # Modelos SQLAlchemy
├── main.py                         # FastAPI endpoints
├── requirements.txt                # Dependencias Python
├── .env.example                    # Variables de entorno
├── postman_collection_completo.json # Colección Postman
└── README.md                       # Este archivo
```

### Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **PostgreSQL**: Base de datos relacional (Render)
- **SQLAlchemy**: ORM para Python
- **Google Gemini AI**: Modelos de IA generativa
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

### Modelos de Base de Datos

#### Usuario
```python
- id, nombre, email
- ingreso_mensual, objetivo_ahorro
- creado_en, actualizado_en
```

#### Transacción
```python
- id, usuario_id, tipo (ingreso/gasto)
- categoria, monto, descripcion
- fecha, creado_en
```

#### Presupuesto
```python
- id, usuario_id, categoria
- monto_limite, monto_gastado
- mes, anio, actualizado_en
```

#### Alerta
```python
- id, usuario_id, nivel, estado
- titulo, mensaje, metadata
- creado_en, leido_en
```

#### AnalisisFinanciero
```python
- id, usuario_id
- periodo_inicio, periodo_fin
- total_ingresos, total_gastos, balance
- recomendaciones, analisis_ia
```

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <tu-repositorio>
cd Protocolos_tarea
```

### 2. Crear Entorno Virtual
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
cp .env.example .env
```

Editar `.env` y agregar:
```env
DATABASE_URL=postgresql://finanzas_zz74_user:OY8LbDEk5eUbY9qJWtuRwnTy956vEOV0@dpg-d498208dl3ps73fr5cq0-a.oregon-postgres.render.com/finanzas_zz74
GOOGLE_API_KEY=tu_api_key_de_google_ai_studio
```

**Obtener API Key de Google**: https://makersuite.google.com/app/apikey

### 5. Iniciar el Servidor
```bash
uvicorn main:app --reload --port 8000
```

La API estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

## 🧪 Pruebas

### Pruebas con Postman

1. Importar la colección `postman_collection_completo.json` en Postman
2. La variable `{{base_url}}` está configurada como `http://localhost:8000`
3. Para Render, cambiar a: `https://tu-app.onrender.com`

### Secuencia de Pruebas Recomendada

#### 1. Verificar Sistema
```
GET /
GET /health
GET /monitor/status
```

#### 2. Crear Usuario
```
POST /usuarios
{
  "nombre": "Juan Pérez",
  "email": "juan@email.com",
  "ingreso_mensual": 50000.0,
  "objetivo_ahorro": 10000.0
}
```

#### 3. Crear Presupuestos
```
POST /presupuestos (Alimentación: 5000)
POST /presupuestos (Transporte: 3000)
POST /presupuestos (Entretenimiento: 2000)
```

#### 4. Registrar Transacciones
```
POST /transacciones (Ingreso: 50000)
POST /transacciones (Gasto Alimentación: 1500)
POST /transacciones (Gasto Transporte: 800)
```

#### 5. Análisis con IA
```
POST /analisis/balance         # Agente Ejecutor (ACP)
POST /analisis/presupuestos    # Agente Ejecutor (ACP)
POST /analisis/completo        # Agente Planificador (ANP)
POST /recomendaciones          # Knowledge Base (MCP)
```

#### 6. Visualización
```
GET /dashboard/1               # Agente Interfaz (AGUI)
GET /alertas?usuario_id=1
```

### Endpoints Principales

| Método | Endpoint | Descripción | Protocolo |
|--------|----------|-------------|-----------|
| GET | `/` | Info del sistema | - |
| GET | `/health` | Estado de salud | - |
| POST | `/usuarios` | Crear usuario | - |
| GET | `/usuarios` | Listar usuarios | - |
| POST | `/transacciones` | Crear transacción | A2A |
| GET | `/transacciones` | Listar transacciones | - |
| POST | `/presupuestos` | Crear presupuesto | ANP |
| GET | `/presupuestos` | Listar presupuestos | - |
| GET | `/alertas` | Listar alertas | - |
| POST | `/analisis/balance` | Analizar balance | ACP |
| POST | `/analisis/presupuestos` | Verificar presupuestos | ACP |
| POST | `/analisis/completo` | Análisis completo | ANP |
| POST | `/recomendaciones` | Obtener recomendaciones | MCP |
| GET | `/dashboard/{id}` | Dashboard completo | AGUI |
| GET | `/monitor/status` | Estado del sistema | - |

## 📊 Ejemplo de Uso Completo

### Escenario: Usuario quiere analizar sus finanzas

1. **Frontend solicita análisis completo**
   ```bash
   POST /analisis/completo
   {
     "usuario_id": 1,
     "periodo_dias": 30
   }
   ```

2. **Planificador descompone la tarea (ANP)**
   - Subtarea 1: Calcular balance → Ejecutor
   - Subtarea 2: Verificar presupuestos → Ejecutor
   - Subtarea 3: Generar alertas → Notificador

3. **Ejecutor consulta datos (ACP)**
   ```python
   # Comunicación con Knowledge Base
   ejecutor.send_message(
       to_agent="KnowledgeBase",
       protocol="ACP",
       message_type="QUERY_TRANSACTIONS",
       content={"usuario_id": 1, "periodo_dias": 30}
   )
   ```

4. **Knowledge Base retorna datos (MCP)**
   ```python
   # Datos con esquema estandarizado
   {
       "protocol": "MCP",
       "content_type": "transaction_query_result",
       "data": {...}
   }
   ```

5. **Notificador genera alertas (A2A)**
   ```python
   # Si presupuesto excede 80%
   notificador.send_message(
       to_agent="Interfaz",
       protocol="A2A",
       message_type="ALERT_REQUIRED",
       content={...}
   )
   ```

6. **Interfaz formatea para UI (AGUI)**
   ```python
   # Formato optimizado para frontend
   interfaz.create_dashboard({
       "usuario_id": 1,
       "datos": {...}
   })
   ```

## 🌐 Despliegue en Render

### 1. Preparar para Producción

Crear `render.yaml`:
```yaml
services:
  - type: web
    name: finanzas-multiagente
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: finanzas_zz74
          property: connectionString
      - key: GOOGLE_API_KEY
        sync: false
```

### 2. Configurar en Render

1. Conectar repositorio de GitHub
2. Seleccionar "Web Service"
3. Agregar variable de entorno `GOOGLE_API_KEY`
4. La base de datos PostgreSQL ya está configurada

### 3. Verificar Despliegue

```bash
curl https://tu-app.onrender.com/health
```

## 📝 Conclusiones

### Logros Principales

1. ✅ **Arquitectura Multiagente Funcional**: Sistema con 6 agentes especializados trabajando en colaboración
2. ✅ **Protocolos Implementados**: 5 protocolos diferentes (A2A, ACP, ANP, AGUI, MCP) con casos de uso específicos
3. ✅ **Integración con IA**: Uso de Google Gemini para análisis inteligente y recomendaciones
4. ✅ **API REST Completa**: FastAPI con documentación automática y validación de datos
5. ✅ **Persistencia de Datos**: PostgreSQL en Render con modelos relacionales
6. ✅ **Escalabilidad**: Diseño modular que permite agregar nuevos agentes y protocolos

### Aprendizajes Clave

- **Comunicación entre Agentes**: Los protocolos estandarizados facilitan la coordinación y mantenimiento
- **División de Responsabilidades**: Cada agente tiene un rol específico, mejorando la modularidad
- **IA como Herramienta**: Los modelos Gemini potencian las capacidades de análisis sin complejidad excesiva
- **Diseño de APIs**: FastAPI permite desarrollo rápido con validación automática

### Mejoras Futuras

- [ ] Implementar autenticación JWT
- [ ] Agregar más análisis predictivos con IA
- [ ] Dashboard web interactivo (React/Vue)
- [ ] Notificaciones en tiempo real (WebSockets)
- [ ] Tests unitarios y de integración
- [ ] Caché con Redis para optimización
- [ ] Métricas y logging avanzado

## 📚 Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini AI](https://ai.google.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [FIPA Agent Communication](http://www.fipa.org/specs/fipa00061/)
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)

## 📞 Contacto y Soporte

Para preguntas o sugerencias sobre este proyecto:
- Issues en GitHub
- Documentación interactiva: `/docs` endpoint

---

**Desarrollado con ❤️ usando FastAPI, Google Gemini AI y PostgreSQL**
