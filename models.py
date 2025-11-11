from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum

# Enumeraciones
class TipoTransaccion(str, enum.Enum):
    INGRESO = "ingreso"
    GASTO = "gasto"

class CategoriaGasto(str, enum.Enum):
    ALIMENTACION = "alimentacion"
    TRANSPORTE = "transporte"
    VIVIENDA = "vivienda"
    ENTRETENIMIENTO = "entretenimiento"
    SALUD = "salud"
    EDUCACION = "educacion"
    SERVICIOS = "servicios"
    OTROS = "otros"

class EstadoAlerta(str, enum.Enum):
    PENDIENTE = "pendiente"
    LEIDA = "leida"
    RESUELTA = "resuelta"

class NivelAlerta(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class TipoAgente(str, enum.Enum):
    PLANIFICADOR = "planificador"
    EJECUTOR = "ejecutor"
    NOTIFICADOR = "notificador"
    INTERFAZ = "interfaz"
    KNOWLEDGE_BASE = "knowledge_base"
    MONITOR = "monitor"

# Modelos
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    ingreso_mensual = Column(Float, default=0.0)
    objetivo_ahorro = Column(Float, default=0.0)
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    transacciones = relationship("Transaccion", back_populates="usuario", cascade="all, delete-orphan")
    presupuestos = relationship("Presupuesto", back_populates="usuario", cascade="all, delete-orphan")
    alertas = relationship("Alerta", back_populates="usuario", cascade="all, delete-orphan")
    analisis = relationship("AnalisisFinanciero", back_populates="usuario", cascade="all, delete-orphan")

class Transaccion(Base):
    __tablename__ = "transacciones"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(SQLEnum(TipoTransaccion), nullable=False)
    categoria = Column(SQLEnum(CategoriaGasto), nullable=True)
    monto = Column(Float, nullable=False)
    descripcion = Column(String(200), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    creado_en = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="transacciones")

class Presupuesto(Base):
    __tablename__ = "presupuestos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    categoria = Column(SQLEnum(CategoriaGasto), nullable=False)
    monto_limite = Column(Float, nullable=False)
    monto_gastado = Column(Float, default=0.0)
    mes = Column(Integer, nullable=False)  # 1-12
    anio = Column(Integer, nullable=False)
    creado_en = Column(DateTime, default=datetime.utcnow)
    actualizado_en = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="presupuestos")

class Alerta(Base):
    __tablename__ = "alertas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    nivel = Column(SQLEnum(NivelAlerta), nullable=False)
    estado = Column(SQLEnum(EstadoAlerta), default=EstadoAlerta.PENDIENTE)
    titulo = Column(String(200), nullable=False)
    mensaje = Column(Text, nullable=False)
    datos_extra = Column(Text, nullable=True)  # JSON string
    creado_en = Column(DateTime, default=datetime.utcnow)
    leido_en = Column(DateTime, nullable=True)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="alertas")

class AnalisisFinanciero(Base):
    __tablename__ = "analisis_financieros"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    periodo_inicio = Column(DateTime, nullable=False)
    periodo_fin = Column(DateTime, nullable=False)
    total_ingresos = Column(Float, default=0.0)
    total_gastos = Column(Float, default=0.0)
    balance = Column(Float, default=0.0)
    recomendaciones = Column(Text, nullable=True)  # JSON string
    analisis_ia = Column(Text, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="analisis")

class LogAgente(Base):
    __tablename__ = "logs_agentes"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo_agente = Column(SQLEnum(TipoAgente), nullable=False)
    accion = Column(String(100), nullable=False)
    protocolo_usado = Column(String(50), nullable=True)
    mensaje_enviado = Column(Text, nullable=True)
    mensaje_recibido = Column(Text, nullable=True)
    datos_extra = Column(Text, nullable=True)  # JSON string
    exito = Column(Boolean, default=True)
    error = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
