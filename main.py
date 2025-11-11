from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import logging

# Importaciones locales
from database import get_db, init_db, test_connection
from models import (
    Usuario, Transaccion, Presupuesto, Alerta, AnalisisFinanciero, LogAgente,
    TipoTransaccion, CategoriaGasto, EstadoAlerta, NivelAlerta, TipoAgente
)
from config import APP_NAME, APP_VERSION, GOOGLE_API_KEY

# Importar agentes
from agentes.planificador_agent import PlanificadorAgent
from agentes.ejecutor_agent import EjecutorAgent
from agentes.notificador_agent import NotificadorAgent
from agentes.interfaz_agent import InterfazAgent
from agentes.knowledge_base_agent import KnowledgeBaseAgent
from agentes.monitor_agent import MonitorAgent

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Sistema Multiagente de Finanzas Personales usando Google Gemini AI"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar agentes (singleton)
planificador = None
ejecutor = None
notificador = None
interfaz = None
knowledge_base = None
monitor = None

def init_agents():
    """Inicializar todos los agentes del sistema"""
    global planificador, ejecutor, notificador, interfaz, knowledge_base, monitor
    
    if not GOOGLE_API_KEY:
        logger.warning("⚠️ GOOGLE_API_KEY no configurada. Los agentes funcionarán en modo limitado.")
    
    try:
        planificador = PlanificadorAgent()
        ejecutor = EjecutorAgent()
        notificador = NotificadorAgent()
        interfaz = InterfazAgent()
        knowledge_base = KnowledgeBaseAgent()
        monitor = MonitorAgent()
        logger.info("✅ Todos los agentes inicializados correctamente")
    except Exception as e:
        logger.error(f"❌ Error al inicializar agentes: {str(e)}")

# Modelos Pydantic para requests/responses
class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=1, max_length=100)
    ingreso_mensual: float = Field(default=0.0, ge=0)
    objetivo_ahorro: float = Field(default=0.0, ge=0)

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    ingreso_mensual: float
    objetivo_ahorro: float
    creado_en: datetime
    
    class Config:
        from_attributes = True

class TransaccionCreate(BaseModel):
    usuario_id: int
    tipo: TipoTransaccion
    categoria: Optional[CategoriaGasto] = None
    monto: float = Field(..., gt=0)
    descripcion: Optional[str] = None
    fecha: Optional[datetime] = None

class TransaccionResponse(BaseModel):
    id: int
    usuario_id: int
    tipo: TipoTransaccion
    categoria: Optional[CategoriaGasto]
    monto: float
    descripcion: Optional[str]
    fecha: datetime
    
    class Config:
        from_attributes = True

class PresupuestoCreate(BaseModel):
    usuario_id: int
    categoria: CategoriaGasto
    monto_limite: float = Field(..., gt=0)
    mes: int = Field(..., ge=1, le=12)
    anio: int = Field(..., ge=2020)

class PresupuestoResponse(BaseModel):
    id: int
    usuario_id: int
    categoria: CategoriaGasto
    monto_limite: float
    monto_gastado: float
    mes: int
    anio: int
    porcentaje_usado: float = 0.0
    
    class Config:
        from_attributes = True

class AlertaResponse(BaseModel):
    id: int
    usuario_id: int
    nivel: NivelAlerta
    estado: EstadoAlerta
    titulo: str
    mensaje: str
    creado_en: datetime
    
    class Config:
        from_attributes = True

class AnalisisRequest(BaseModel):
    usuario_id: int
    periodo_dias: int = Field(default=30, ge=1, le=365)

class RecomendacionRequest(BaseModel):
    usuario_id: int
    objetivo: str = "optimizar_gastos"

# ===== EVENTOS DE INICIO =====
@app.on_event("startup")
async def startup_event():
    """Inicializar base de datos y agentes al iniciar la aplicación"""
    logger.info("🚀 Iniciando Sistema Multiagente de Finanzas Personales...")
    
    # Probar conexión a base de datos
    if test_connection():
        init_db()
    else:
        logger.error("❌ No se pudo conectar a la base de datos")
    
    # Inicializar agentes
    init_agents()
    
    logger.info("✅ Sistema iniciado correctamente")

# ===== ENDPOINTS DE SALUD =====
@app.get("/")
async def root():
    """Endpoint raíz con información del sistema"""
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "status": "online",
        "agentes": {
            "planificador": "activo" if planificador else "inactivo",
            "ejecutor": "activo" if ejecutor else "inactivo",
            "notificador": "activo" if notificador else "inactivo",
            "interfaz": "activo" if interfaz else "inactivo",
            "knowledge_base": "activo" if knowledge_base else "inactivo",
            "monitor": "activo" if monitor else "inactivo"
        },
        "protocolos": ["A2A", "ACP", "ANP", "AGUI", "MCP"]
    }

@app.get("/health")
async def health_check():
    """Verificar salud del sistema"""
    db_status = test_connection()
    agents_status = all([planificador, ejecutor, notificador, interfaz, knowledge_base, monitor])
    
    return {
        "status": "healthy" if (db_status and agents_status) else "degraded",
        "database": "connected" if db_status else "disconnected",
        "agents": "all_active" if agents_status else "some_inactive",
        "timestamp": datetime.utcnow().isoformat()
    }

# ===== ENDPOINTS DE USUARIOS =====
@app.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear nuevo usuario"""
    # Verificar si el email ya existe
    existing = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    nuevo_usuario = Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    logger.info(f"✅ Usuario creado: {nuevo_usuario.email}")
    return nuevo_usuario

@app.get("/usuarios", response_model=List[UsuarioResponse])
async def listar_usuarios(db: Session = Depends(get_db)):
    """Listar todos los usuarios"""
    usuarios = db.query(Usuario).all()
    return usuarios

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener usuario por ID"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# ===== ENDPOINTS DE TRANSACCIONES =====
@app.post("/transacciones", response_model=TransaccionResponse, status_code=status.HTTP_201_CREATED)
async def crear_transaccion(transaccion: TransaccionCreate, db: Session = Depends(get_db)):
    """
    Crear nueva transacción
    Usa protocolo A2A para notificar al Ejecutor
    """
    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == transaccion.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Crear transacción
    data = transaccion.dict()
    if not data.get('fecha'):
        data['fecha'] = datetime.utcnow()
    
    nueva_transaccion = Transaccion(**data)
    db.add(nueva_transaccion)
    
    # Si es gasto, actualizar presupuesto correspondiente
    if transaccion.tipo == TipoTransaccion.GASTO and transaccion.categoria:
        mes_actual = datetime.utcnow().month
        anio_actual = datetime.utcnow().year
        
        presupuesto = db.query(Presupuesto).filter(
            Presupuesto.usuario_id == transaccion.usuario_id,
            Presupuesto.categoria == transaccion.categoria,
            Presupuesto.mes == mes_actual,
            Presupuesto.anio == anio_actual
        ).first()
        
        if presupuesto:
            presupuesto.monto_gastado += transaccion.monto
            
            # Verificar si se debe generar alerta
            porcentaje = (presupuesto.monto_gastado / presupuesto.monto_limite) * 100
            if porcentaje >= 80 and notificador:
                # Usar protocolo A2A para notificar
                notificador.create_alert({
                    "usuario_id": transaccion.usuario_id,
                    "tipo": "presupuesto_cerca_limite",
                    "datos": {
                        "categoria": transaccion.categoria.value,
                        "porcentaje": porcentaje,
                        "gastado": presupuesto.monto_gastado,
                        "limite": presupuesto.monto_limite
                    }
                })
    
    db.commit()
    db.refresh(nueva_transaccion)
    
    logger.info(f"✅ Transacción creada: {nueva_transaccion.id}")
    return nueva_transaccion

@app.get("/transacciones", response_model=List[TransaccionResponse])
async def listar_transacciones(
    usuario_id: Optional[int] = None,
    tipo: Optional[TipoTransaccion] = None,
    categoria: Optional[CategoriaGasto] = None,
    dias: int = 30,
    db: Session = Depends(get_db)
):
    """Listar transacciones con filtros opcionales"""
    query = db.query(Transaccion)
    
    if usuario_id:
        query = query.filter(Transaccion.usuario_id == usuario_id)
    if tipo:
        query = query.filter(Transaccion.tipo == tipo)
    if categoria:
        query = query.filter(Transaccion.categoria == categoria)
    
    fecha_desde = datetime.utcnow() - timedelta(days=dias)
    query = query.filter(Transaccion.fecha >= fecha_desde)
    
    transacciones = query.order_by(Transaccion.fecha.desc()).all()
    return transacciones

# ===== ENDPOINTS DE PRESUPUESTOS =====
@app.post("/presupuestos", response_model=PresupuestoResponse, status_code=status.HTTP_201_CREATED)
async def crear_presupuesto(presupuesto: PresupuestoCreate, db: Session = Depends(get_db)):
    """
    Crear nuevo presupuesto
    Usa protocolo ANP para distribución de recursos
    """
    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == presupuesto.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar si ya existe presupuesto para esa categoría/periodo
    existing = db.query(Presupuesto).filter(
        Presupuesto.usuario_id == presupuesto.usuario_id,
        Presupuesto.categoria == presupuesto.categoria,
        Presupuesto.mes == presupuesto.mes,
        Presupuesto.anio == presupuesto.anio
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un presupuesto para esta categoría y periodo")
    
    nuevo_presupuesto = Presupuesto(**presupuesto.dict())
    db.add(nuevo_presupuesto)
    db.commit()
    db.refresh(nuevo_presupuesto)
    
    logger.info(f"✅ Presupuesto creado: {nuevo_presupuesto.id}")
    return nuevo_presupuesto

@app.get("/presupuestos", response_model=List[PresupuestoResponse])
async def listar_presupuestos(
    usuario_id: Optional[int] = None,
    mes: Optional[int] = None,
    anio: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar presupuestos con filtros opcionales"""
    query = db.query(Presupuesto)
    
    if usuario_id:
        query = query.filter(Presupuesto.usuario_id == usuario_id)
    if mes:
        query = query.filter(Presupuesto.mes == mes)
    if anio:
        query = query.filter(Presupuesto.anio == anio)
    
    presupuestos = query.all()
    
    # Calcular porcentaje usado
    for p in presupuestos:
        p.porcentaje_usado = (p.monto_gastado / p.monto_limite) * 100 if p.monto_limite > 0 else 0
    
    return presupuestos

@app.get("/presupuestos/{presupuesto_id}", response_model=PresupuestoResponse)
async def obtener_presupuesto(presupuesto_id: int, db: Session = Depends(get_db)):
    """Obtener presupuesto por ID"""
    presupuesto = db.query(Presupuesto).filter(Presupuesto.id == presupuesto_id).first()
    if not presupuesto:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    
    presupuesto.porcentaje_usado = (presupuesto.monto_gastado / presupuesto.monto_limite) * 100
    return presupuesto

# ===== ENDPOINTS DE ALERTAS =====
@app.get("/alertas", response_model=List[AlertaResponse])
async def listar_alertas(
    usuario_id: Optional[int] = None,
    estado: Optional[EstadoAlerta] = None,
    nivel: Optional[NivelAlerta] = None,
    db: Session = Depends(get_db)
):
    """Listar alertas con filtros opcionales"""
    query = db.query(Alerta)
    
    if usuario_id:
        query = query.filter(Alerta.usuario_id == usuario_id)
    if estado:
        query = query.filter(Alerta.estado == estado)
    if nivel:
        query = query.filter(Alerta.nivel == nivel)
    
    alertas = query.order_by(Alerta.creado_en.desc()).all()
    return alertas

@app.patch("/alertas/{alerta_id}/marcar-leida")
async def marcar_alerta_leida(alerta_id: int, db: Session = Depends(get_db)):
    """Marcar alerta como leída"""
    alerta = db.query(Alerta).filter(Alerta.id == alerta_id).first()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    
    alerta.estado = EstadoAlerta.LEIDA
    alerta.leido_en = datetime.utcnow()
    db.commit()
    
    return {"status": "success", "message": "Alerta marcada como leída"}

# ===== ENDPOINTS DE ANÁLISIS CON IA =====
@app.post("/analisis/balance")
async def analizar_balance(request: AnalisisRequest, db: Session = Depends(get_db)):
    """
    Analizar balance financiero usando Agente Ejecutor
    Usa protocolo ACP para comunicación estructurada
    """
    if not ejecutor:
        raise HTTPException(status_code=503, detail="Agente Ejecutor no disponible")
    
    # Verificar usuario
    usuario = db.query(Usuario).filter(Usuario.id == request.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Solicitar análisis usando protocolo ACP
    resultado = ejecutor.calculate_balance({
        "usuario_id": request.usuario_id,
        "periodo_dias": request.periodo_dias
    })
    
    return {
        "status": "success",
        "analisis": resultado,
        "protocol_used": "ACP",
        "agent": "Ejecutor"
    }

@app.post("/analisis/presupuestos")
async def analizar_presupuestos(request: AnalisisRequest, db: Session = Depends(get_db)):
    """
    Verificar estado de presupuestos usando Agente Ejecutor
    Usa protocolo ACP
    """
    if not ejecutor:
        raise HTTPException(status_code=503, detail="Agente Ejecutor no disponible")
    
    resultado = ejecutor.verify_budgets({
        "usuario_id": request.usuario_id
    })
    
    return {
        "status": "success",
        "analisis": resultado,
        "protocol_used": "ACP",
        "agent": "Ejecutor"
    }

@app.post("/analisis/completo")
async def analisis_completo(request: AnalisisRequest, db: Session = Depends(get_db)):
    """
    Análisis financiero completo coordinado por Planificador
    Usa protocolo ANP para distribuir tareas entre agentes
    """
    if not planificador:
        raise HTTPException(status_code=503, detail="Agente Planificador no disponible")
    
    # Planificador coordina el análisis completo
    plan = planificador.create_financial_plan({
        "usuario_id": request.usuario_id,
        "objetivo": "analisis_financiero_completo"
    })
    
    return {
        "status": "success",
        "plan": plan,
        "protocol_used": "ANP",
        "agent": "Planificador",
        "message": "Plan de análisis creado. Las subtareas serán ejecutadas por los agentes correspondientes."
    }

@app.post("/recomendaciones")
async def obtener_recomendaciones(request: RecomendacionRequest, db: Session = Depends(get_db)):
    """
    Obtener recomendaciones financieras usando Knowledge Base
    Usa protocolo MCP para formato estandarizado
    """
    if not knowledge_base:
        raise HTTPException(status_code=503, detail="Agente Knowledge Base no disponible")
    
    insights = knowledge_base.get_spending_insights(
        usuario_id=request.usuario_id
    )
    
    prediccion = knowledge_base.predict_future_expenses(
        usuario_id=request.usuario_id,
        meses_futuros=3
    )
    
    return {
        "status": "success",
        "insights": insights,
        "prediccion": prediccion,
        "protocol_used": "MCP",
        "agent": "KnowledgeBase"
    }

# ===== ENDPOINTS DE INTERFAZ =====
@app.get("/dashboard/{usuario_id}")
async def obtener_dashboard(usuario_id: int, db: Session = Depends(get_db)):
    """
    Obtener dashboard completo del usuario
    Usa protocolo AGUI para formato de interfaz
    """
    if not interfaz:
        raise HTTPException(status_code=503, detail="Agente Interfaz no disponible")
    
    # Verificar usuario
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Recopilar datos
    transacciones = db.query(Transaccion).filter(
        Transaccion.usuario_id == usuario_id
    ).order_by(Transaccion.fecha.desc()).limit(10).all()
    
    presupuestos = db.query(Presupuesto).filter(
        Presupuesto.usuario_id == usuario_id,
        Presupuesto.mes == datetime.utcnow().month,
        Presupuesto.anio == datetime.utcnow().year
    ).all()
    
    alertas = db.query(Alerta).filter(
        Alerta.usuario_id == usuario_id,
        Alerta.estado == EstadoAlerta.PENDIENTE
    ).all()
    
    # Formatear con Agente Interfaz usando AGUI
    dashboard = interfaz.create_dashboard({
        "usuario_id": usuario_id,
        "datos": {
            "usuario": {
                "nombre": usuario.nombre,
                "email": usuario.email,
                "ingreso_mensual": usuario.ingreso_mensual
            },
            "transacciones_recientes": len(transacciones),
            "presupuestos_activos": len(presupuestos),
            "alertas_pendientes": len(alertas)
        }
    })
    
    return {
        "status": "success",
        "dashboard": dashboard,
        "protocol_used": "AGUI",
        "agent": "Interfaz"
    }

# ===== ENDPOINTS DE MONITOREO =====
@app.get("/monitor/status")
async def obtener_status_sistema():
    """Obtener status del sistema multiagente"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Agente Monitor no disponible")
    
    health = monitor.check_system_health()
    metrics = monitor.get_system_metrics()
    
    return {
        "health": health,
        "metrics": metrics,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/monitor/agentes")
async def obtener_status_agentes():
    """Obtener status de todos los agentes"""
    return {
        "agentes": {
            "planificador": {
                "activo": planificador is not None,
                "historial": len(planificador.get_history()) if planificador else 0
            },
            "ejecutor": {
                "activo": ejecutor is not None,
                "historial": len(ejecutor.get_history()) if ejecutor else 0
            },
            "notificador": {
                "activo": notificador is not None,
                "historial": len(notificador.get_history()) if notificador else 0
            },
            "interfaz": {
                "activo": interfaz is not None,
                "historial": len(interfaz.get_history()) if interfaz else 0
            },
            "knowledge_base": {
                "activo": knowledge_base is not None,
                "historial": len(knowledge_base.get_history()) if knowledge_base else 0
            },
            "monitor": {
                "activo": monitor is not None,
                "historial": len(monitor.get_history()) if monitor else 0
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
