# 🚀 Guía Rápida de Inicio

## Instalación Rápida (5 minutos)

### 1. Clonar y Preparar
```bash
cd Protocolos_tarea
python -m venv venv
```

### 2. Activar Entorno Virtual

**Windows:**
```powershell
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu GOOGLE_API_KEY
# Obtener en: https://makersuite.google.com/app/apikey
```

### 5. Probar el Sistema
```bash
python test_sistema.py
```

### 6. Iniciar el Servidor
```bash
uvicorn main:app --reload --port 8000
```

### 7. Abrir Documentación
```
http://localhost:8000/docs
```

## Pruebas Rápidas con Postman

### Importar Colección
1. Abrir Postman
2. Import → File → `postman_collection_completo.json`
3. La variable `{{base_url}}` ya está configurada

### Flujo de Prueba Básico

#### 1. Verificar Sistema
```
GET /
GET /health
```

#### 2. Crear Usuario
```
POST /usuarios
Body:
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
POST /transacciones (Gasto Alimentación: 4500)
```

#### 5. Análisis con IA
```
POST /analisis/completo
Body:
{
  "usuario_id": 1,
  "periodo_dias": 30
}
```

#### 6. Dashboard
```
GET /dashboard/1
```

## Comandos Útiles

### Verificar Logs
```bash
# Ver logs en tiempo real
uvicorn main:app --reload --log-level debug
```

### Reiniciar Base de Datos
```bash
# En main.py, init_db() crea todas las tablas
python -c "from database import init_db; init_db()"
```

### Probar Agente Individual
```python
from agentes import PlanificadorAgent

planificador = PlanificadorAgent()
resultado = planificador.create_financial_plan({
    "usuario_id": 1,
    "objetivo": "analizar_finanzas"
})
print(resultado)
```

## Endpoints Esenciales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Información del sistema |
| `/health` | GET | Estado de salud |
| `/usuarios` | POST | Crear usuario |
| `/transacciones` | POST | Registrar transacción |
| `/presupuestos` | POST | Crear presupuesto |
| `/analisis/completo` | POST | Análisis completo con IA |
| `/dashboard/{id}` | GET | Dashboard del usuario |
| `/monitor/status` | GET | Estado del sistema |

## Solución de Problemas

### Error: No se puede conectar a PostgreSQL
```bash
# Verificar que DATABASE_URL esté en .env
# Verificar que la conexión de Render esté activa
python test_sistema.py
```

### Error: GOOGLE_API_KEY no configurada
```bash
# 1. Obtener key en: https://makersuite.google.com/app/apikey
# 2. Agregar en .env:
GOOGLE_API_KEY=tu_key_aqui
```

### Error: Módulo no encontrado
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Puerto 8000 ocupado
```bash
# Usar otro puerto
uvicorn main:app --reload --port 8001
```

## Arquitectura Rápida

```
Sistema Multiagente
├── 6 Agentes (Gemini AI)
│   ├── Planificador (ANP)
│   ├── Ejecutor (ACP)
│   ├── Notificador (A2A)
│   ├── Interfaz (AGUI)
│   ├── Knowledge Base (MCP)
│   └── Monitor
├── 5 Protocolos
│   ├── A2A: Comunicación general
│   ├── ACP: Mensajes estructurados
│   ├── ANP: Negociación de tareas
│   ├── AGUI: Interfaz de usuario
│   └── MCP: Contenido estandarizado
└── PostgreSQL (Render)
```

## Recursos Adicionales

- 📖 **README.md**: Documentación completa
- 📊 **DOCUMENTACION_TECNICA.md**: Flujos detallados
- 🧪 **test_sistema.py**: Verificación del sistema
- 📮 **postman_collection_completo.json**: Pruebas API

## Siguiente Paso: Deploy en Render

```bash
# 1. Commit cambios
git add .
git commit -m "Sistema multiagente completo"
git push

# 2. En Render:
# - Conectar repositorio
# - Tipo: Web Service
# - Agregar GOOGLE_API_KEY en Environment
# - Deploy automático
```

---

**¿Necesitas ayuda?** Revisa `/docs` para documentación interactiva de la API.
